from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import sys

# Проверяем, поддерживается ли OpenMP
def check_openmp():
    """Проверяет, поддерживает ли компилятор OpenMP."""
    import subprocess
    import os
    
    # Для Windows
    if sys.platform == "win32":
        return True  # MSVC обычно поддерживает OpenMP

# Флаги для OpenMP
if sys.platform == "win32":
    omp_args = ['/openmp']
else:
    omp_args = ['-fopenmp']

# Определяем расширение
extensions = [
    Extension(
        "integrate_5_cy",
        ["integrate_5_cy.pyx"],
        extra_compile_args=omp_args,
        extra_link_args=omp_args,
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    )
]

setup(
    name="integrate_5_nogil",
    ext_modules=cythonize(
        extensions,
        annotate=True,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'initializedcheck': False,
            'nonecheck': False,
            'cdivision': True,
            'embedsignature': True,
        }
    ),
    include_dirs=[np.get_include()],
)