import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyenrichr",
    version="1.0.2",
    author="Alexander Lachmann",
    author_email="alexander.lachmann@mssm.edu",
    description="Official Enrichr Python package for fast local gene set enrichment.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maayanlab/pyenrichr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "pyenrichr": ["data/*"]
    },
    include_package_data=True,
    install_requires=[
        'pandas>=1.1.5',
        'numpy',
        'statsmodels',
        'numba',
        'python-louvain',
        'networkx',
        'tqdm'
    ],
    python_requires='>=3.6',
)
