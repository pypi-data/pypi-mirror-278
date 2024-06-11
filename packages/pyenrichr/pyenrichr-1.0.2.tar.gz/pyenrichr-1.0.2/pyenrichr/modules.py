import networkx as nx
import community as community_louvain
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

def detect(adjacency, random_state=1):
    pmat = np.log(adjacency)
    pmat[pmat < -100] = -100
    pmat = -pmat
    G = nx.from_pandas_adjacency(pmat)
    partition = community_louvain.best_partition(G, random_state=random_state)
    return partition

def genes(library, terms):
    return Counter(gene for term in terms if term in library for gene in library[term])

def terms(id, partition):
    return [k for k, v in partition.items() if v == id]

def plot(terms, pmat):
    adj = -np.log(pmat.loc[terms, terms])
    adj[adj > 100] = 100
    G = nx.from_pandas_adjacency(adj)
    
    plt.figure(figsize=(8, 8))
    nx.draw(G, with_labels=True, node_color='lightblue', node_size=2000, font_size=15, font_weight='bold', edge_color='gray')
    plt.title("Network Graph from Adjacency DataFrame")
    plt.show()
