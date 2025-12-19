# setup_4.py
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Определяем расширение
extensions = [
    Extension(
        "integrate_4_cy",
        ["integrate_4_cy.pyx"],
        extra_compile_args=['/openmp' if hasattr(Extension, 'msvc') else '-fopenmp'],
        extra_link_args=['/openmp' if hasattr(Extension, 'msvc') else '-fopenmp'],
    )
]

setup(
    name="integrate_4_cy",
    ext_modules=cythonize(extensions, annotate=True, compiler_directives={
        'language_level': "3",
        'boundscheck': False,
        'wraparound': False,
        'initializedcheck': False,
        'nonecheck': False,
        'cdivision': True,
    }),
    include_dirs=[np.get_include()],
)

# from setuptools import setup
# from Cython.Build import cythonize
# import numpy

# setup(
#     ext_modules=cythonize(
#         "integrate_4_cy.pyx",
#         compiler_directives={
#             'language_level': "3",
#             'boundscheck': False,
#             'wraparound': False,
#             'initializedcheck': False,
#             'nonecheck': False,
#             'cdivision': True,
#         },
#         annotate=True  # Генерируем HTML аннотации
#     ),
#     include_dirs=[numpy.get_include()] if numpy else [],
# )