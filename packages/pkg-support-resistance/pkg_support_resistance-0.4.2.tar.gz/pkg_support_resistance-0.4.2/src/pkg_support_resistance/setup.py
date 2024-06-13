"""
Setup module.
> Execute setup:
> cd pkg_support_resistance (root)
> python setup.py build_ext --inplace
"""

from setuptools import setup, Extension

from Cython.Build import cythonize
import numpy as np


ext_modules = [
    Extension(
        "vanilla.vanilla_algo",
        sources=["vanilla/vanilla_algo.c"],
    ),
    Extension(
        "kmeans.kmeans_algo",
        sources=["kmeans/kmeans_algo.c"],
    ),
    Extension(
        "dbscan.dbscan_algo",
        sources=["dbscan/dbscan_algo.c"],
    ),
]

setup(
    name="pkg_support_resistance",
    ext_modules=cythonize(ext_modules),
    include_dirs=[np.get_include()],
)
