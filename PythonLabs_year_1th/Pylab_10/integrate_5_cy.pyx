# integrate_5_cy.pyx
import cython
from cython import boundscheck, wraparound, cdivision, nogil
from libc.math cimport cos, sin, pow
from cython.parallel cimport prange, parallel

# Структура для хранения промежуточных результатов в многопоточном режиме
cdef struct Result:
    double value
    int thread_id

# Версия с отключенным GIL для использования в потоках
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef double integrate_nogil_inner(str func_name, double a, double b, int n_iter) nogil:
    """
    Внутренняя функция, которая может выполняться без GIL.
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
    elif func_name == "cube":
        for i in range(n_iter):
            x = a + i * step
            acc += (x * x * x) * step
    
    return acc

# Обертка Python для функции с nogil
def integrate_nogil(func_name: str, double a, double b, int n_iter=100000):
    """
    Python-обертка для функции с nogil.
    """
    return integrate_nogil_inner(func_name, a, b, n_iter)

# Версия с использованием OpenMP (если доступно) - исправленная
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef double integrate_openmp_inner(str func_name, double a, double b, int n_iter) nogil:
    """
    Версия с использованием OpenMP для автоматического распараллеливания.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    
    if func_name == "cos":
        # Используем директиву OpenMP для распараллеливания
        for i in prange(n_iter, nogil=True, schedule='guided'):
            x = a + i * step
            acc += cos(x) * step
    elif func_name == "sin":
        for i in prange(n_iter, nogil=True, schedule='guided'):
            x = a + i * step
            acc += sin(x) * step
    elif func_name == "square":
        for i in prange(n_iter, nogil=True, schedule='guided'):
            x = a + i * step
            acc += (x * x) * step
    
    return acc

def integrate_openmp(func_name: str, double a, double b, int n_iter=100000):
    """
    Python-обертка для OpenMP версии.
    """
    return integrate_openmp_inner(func_name, a, b, n_iter)

# Альтернативная версия OpenMP с reduction
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef double integrate_openmp_reduction_inner(str func_name, double a, double b, int n_iter) nogil:
    """
    Версия OpenMP с использованием редукции для суммы.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    
    if func_name == "cos":
        with nogil, parallel():
            for i in prange(n_iter, schedule='guided'):
                x = a + i * step
                acc += cos(x) * step
    elif func_name == "sin":
        with nogil, parallel():
            for i in prange(n_iter, schedule='guided'):
                x = a + i * step
                acc += sin(x) * step
    elif func_name == "square":
        with nogil, parallel():
            for i in prange(n_iter, schedule='guided'):
                x = a + i * step
                acc += x * x * step
    
    return acc

def integrate_openmp_reduction(func_name: str, double a, double b, int n_iter=100000):
    """
    Python-обертка для OpenMP версии с редукцией.
    """
    return integrate_openmp_reduction_inner(func_name, a, b, n_iter)

# Функция для тестирования точности
def test_nogil_accuracy():
    """Тест точности nogil версии."""
    import math
    
    print("Тест точности nogil версии:")
    print("-" * 50)
    
    test_cases = [
        ("cos", 0, math.pi/2, 1.0),
        ("sin", 0, math.pi, 2.0),
        ("square", 0, 1, 1/3),
    ]
    
    for func_name, a, b, expected in test_cases:
        result = integrate_nogil(func_name, a, b, 10000)
        error = abs(result - expected)
        print(f"{func_name}: {result:.6f} (ожидается {expected:.6f}, ошибка: {error:.2e})")