from numba import float64, int64, njit, prange
from numba.experimental import jitclass
from math import log, exp
import numpy as np
import pandas as pd
import tqdm
from statsmodels.stats.multitest import multipletests

from pyenrichr.libraries import vectorize

# Define the structure of our jit class
spec = [
    ('f', float64[:]),  # Vector of doubles
    ('max_size', int64) # Integer
]

@jitclass(spec)
class FastFisher:
    def __init__(self, max_size):
        self.f = np.zeros(max_size + 1, dtype=np.float64)
        self.max_size = max_size
        for i in range(1, max_size + 1):
            self.f[i] = self.f[i - 1] + log(i)

    def get_p(self, a, b, c, d, same):
        return exp(same - (self.f[a] + self.f[b] + self.f[c] + self.f[d]))

    def get_p_value(self, a, b, c, d):
        n = a + b + c + d
        if n > self.max_size:
            return np.nan
        same = self.f[a + b] + self.f[c + d] + self.f[a + c] + self.f[b + d] - self.f[n]
        p = self.get_p(a, b, c, d, same)
        
        minimum = min(c, b)
        for _ in range(minimum):
            a += 1
            b -= 1
            c -= 1
            d += 1
            p += self.get_p(a, b, c, d, same)
        return p

@njit(parallel=True)
def get_p_value_list(fisher, contingency_tables):
    num_tests = contingency_tables.shape[0]
    results = np.empty(num_tests, dtype=np.float64)
    for i in prange(num_tests):
        a, b, c, d = contingency_tables[i]
        p_value = fisher.get_p_value(a, b, c, d)
        results[i] = p_value
    return results

def is_library(var):
    if isinstance(var, dict):
        return all(isinstance(value, set) for value in var.values()) 
    return False 

def fisher(gene_set, library, fisher=None, min_set_size=5, min_overlap=2, uppercase=True, background_size=22000, verbose=True):
    if fisher == None:
        all = {element for subset in library.values() for element in subset}
        fisher = FastFisher(max(len(all)+1000, background_size+4000))
    
    if is_library(gene_set):
        vec_lib = vectorize(library)
        lib_length = np.array([len(library[x]) for x in library])
        k = list(gene_set.keys())[0]

        enrichments = {}
        for k in tqdm.tqdm(gene_set, disable=not verbose):
            temp_gs = gene_set[k]
            if uppercase:
                temp_gs = {string.upper() for string in temp_gs}
            enrichments[k] = fastfisher(temp_gs, vec_lib, lib_length, fisher=fisher, min_overlap=min_overlap, min_set_size=min_set_size, background_size=background_size, verbose=verbose)
        return enrichments
    
    if uppercase:
        gene_set = {string.upper() for string in gene_set}
    
    lib_size = len(library)
    library_keys = list(library.keys())
    l1 = np.repeat(len(gene_set), lib_size)
    l3 = np.repeat(background_size, lib_size)

    overlap = np.array([library[x].intersection(gene_set) for x in library_keys])
    a = np.array([len(x) for x in overlap])
    overlap = np.array([",".join(x) for x in overlap])

    l2 = np.array([len(library[x]) for x in library_keys])

    b = l1 - a
    c = l2 - a
    d = l3 - b - c + a

    contingency = np.array([a,b,c,d]).T

    relevant_idx = np.where((a >= min_overlap) & (l2 >= min_set_size))[0]
    odds = (a[relevant_idx] / l1[relevant_idx]) / (l2[relevant_idx] / l3[relevant_idx])

    p_values = get_p_value_list(fisher, contingency[relevant_idx, :])
    fdr_corrected_pvals = []
    sidak_corrected_pvals = []

    if len(p_values) > 0:
        _, fdr_corrected_pvals, _, _ = multipletests(p_values, method='fdr_bh')
        _, sidak_corrected_pvals, _, _ = multipletests(p_values, method='sidak')

    result = pd.DataFrame({
        "term": np.array(library_keys, dtype=object)[relevant_idx],
        "p-value": np.array(p_values, dtype='float64'),
        "sidak": np.array(sidak_corrected_pvals, dtype='float64'),
        "fdr": np.array(fdr_corrected_pvals, dtype='float64'),
        "odds": np.array(odds, dtype='float64'),
        "overlap": a[relevant_idx], 
        "set-size": l2[relevant_idx].astype('int32'),
        "gene-overlap": overlap[relevant_idx]
    })
    
    result.sort_values("p-value", inplace=True)
    result.index = np.arange(1, len(result.index)+1)
    
    return result

def convert_gene_set(gene_set, lib_lookup):
    bit_set = np.zeros(len(lib_lookup) + 1, dtype=np.int64)
    for g in gene_set:
        if g in lib_lookup:
            bit_set[lib_lookup[g]] = 1
    return bit_set

@njit
def map_gene_overlap(gene_set, typed_lib):
    overlap = np.zeros(len(typed_lib), dtype=np.int64)
    for i, k in enumerate(typed_lib):
       gset = typed_lib[k]
       for g in gset:
           overlap[i] += gene_set[g]
    return overlap

def fastfisher(gene_set, library, set_sizes, fisher=None, min_set_size=5, min_overlap=2, background_size=22000, verbose=True):
    if fisher == None:
        fisher = FastFisher(44000)
    types_gene_lookup = library["genes"]
    typed_lib = library["library"]
    lib_size = len(typed_lib)
    library_keys = list(typed_lib.keys())
    l1 = np.repeat(len(gene_set), lib_size)
    l3 = np.repeat(background_size, lib_size)
    
    gene_set = convert_gene_set(gene_set, types_gene_lookup)
    a = map_gene_overlap(gene_set, typed_lib)
    
    b = l1 - a
    c = set_sizes - a
    d = l3 - b - c + a

    contingency = np.array([a,b,c,d]).T
    
    relevant_idx = np.where((a >= min_overlap) & (set_sizes >= min_set_size))[0]
    odds = (a[relevant_idx] / l1[relevant_idx]) / (set_sizes[relevant_idx] / l3[relevant_idx])

    p_values = get_p_value_list(fisher, contingency[relevant_idx, :])
    
    fdr_corrected_pvals = []
    sidak_corrected_pvals = []

    if len(p_values) > 0:
        _, fdr_corrected_pvals, _, _ = multipletests(p_values, method='fdr_bh')
        _, sidak_corrected_pvals, _, _ = multipletests(p_values, method='sidak')

    result = pd.DataFrame({
        "term": np.array(library_keys, dtype=object)[relevant_idx],
        "p-value": np.array(p_values, dtype='float64'),
        "sidak": np.array(sidak_corrected_pvals, dtype='float64'),
        "fdr": np.array(fdr_corrected_pvals, dtype='float64'),
        "odds": np.array(odds, dtype='float64'),
        "overlap": a[relevant_idx], 
        "set-size": set_sizes[relevant_idx].astype('int32')
    })

    result.sort_values("p-value", inplace=True)
    result.index = np.arange(1, len(result.index)+1)

    return result

def consolidate(result):
    res = []
    keys = list(result.keys())
    for k in keys:
        temp = result[k].iloc[:,0:2]
        temp = temp.set_index("term")
        res.append(temp)
    temp = pd.concat(res, axis=1).fillna(1)
    temp.columns = keys
    return temp