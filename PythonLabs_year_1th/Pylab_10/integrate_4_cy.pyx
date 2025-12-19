# integrate_4_cy.pyx
import cython
from cython import boundscheck, wraparound, cdivision
from libc.math cimport cos, sin, fabs

# Отключаем проверки для скорости
@boundscheck(False)
@wraparound(False)
@cdivision(True)
def integrate_cython(func_name: str, double a, double b, int n_iter=100000):
    """
    Оптимизированная версия функции интегрирования на Cython.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double x
    cdef int i
    
    if func_name == "cos":
        for i in range(n_iter):
            x = a + i * step
            acc += cos(x) * step
    elif func_name == "sin":
        for i in range(n_iter):
            x = a + i * step
            acc += sin(x) * step
    elif func_name == "square":
        for i in range(n_iter):
            x = a + i * step
            acc += (x * x) * step
    else:
        raise ValueError(f"Unknown function: {func_name}")
    
    return acc