# итерация 4

# профилирование и оптимизация функции integrate
# оптимизировать функцию integrate с помощью Cython
# замерить время вычисления функции без потоков и процессов (сравнить с итерацией 1)
# замерить время вычисления с потоками и процессами (сравнить с итерациями 2 и 3 соответственно)
# использовать annotate = True получить html-файл для модуля integrate и максимально
# оптимировать код для уменьшения взаимодействия с C-API

import math
import time
import timeit
import statistics
import matplotlib.pyplot as plt
from typing import Callable, List, Tuple
import concurrent.futures as ftres
from functools import partial
import multiprocessing as mp
import sys
import os

# Импортируем Cython модуль (после компиляции)
# CYTHON_AVAILABLE = False
# integrate_cython = None

# try:
#     # Попробуйте импортировать напрямую (если модуль уже скомпилирован)
#     import integrate_4_cy
#     integrate_cython = integrate_4_cy.integrate_cython
#     CYTHON_AVAILABLE = True
#     print("✓ Cython модуль успешно загружен")
# except ImportError:
#     print("Cython модуль не найден. Попытка скомпилировать...")
    
#     # Попробуем скомпилировать на лету
#     try:
#         import pyximport
#         import numpy
#         pyximport.install(
#             language_level=3,
#             setup_args={
#                 'include_dirs': numpy.get_include(),
#             }
#         )
        
#         # Теперь импортируем
#         import integrate_4_cy
#         integrate_cython = integrate_4_cy.integrate_cython
#         CYTHON_AVAILABLE = True
#         print("✓ Cython модуль скомпилирован и загружен")
#     except Exception as e:
#         print(f"✗ Не удалось скомпилировать Cython модуль: {e}")
#         print("Продолжаем только с Python версиями...")

# import pyximport
# import numpy
# pyximport.install(
#     language_level=3,
#     setup_args={
#         'include_dirs': numpy.get_include(),
#     }
# )

# Теперь импортируем
import integrate_4_cy
integrate_cython = integrate_4_cy.integrate_cython
CYTHON_AVAILABLE = True
# print("✓ Cython модуль скомпилирован и загружен")

# def integrate_threaded_cython(func_name: str,
def integrate_4(func_name: str, a: float, b: float, *, n_iter: int = 100000, n_threads: int = 4) -> float:
    """Многопоточная версия с Cython (использует ThreadPoolExecutor)."""
    if not CYTHON_AVAILABLE:
        raise RuntimeError("Cython module not available")
    
    with ftres.ThreadPoolExecutor(max_workers=n_threads) as executor:
        chunk_iter = n_iter // n_threads
        step = (b - a) / n_threads
        
        # Создаем список задач для каждого потока
        futures = []
        for i in range(n_threads):
            a_i = a + i * step
            b_i = a + (i + 1) * step if i < n_threads - 1 else b
            
            func_name = func_name.split("math.")[1] if "math" in func_name else func_name
            # Передаем аргументы правильно
            future = executor.submit(integrate_cython, func_name, a_i, b_i, chunk_iter)
            futures.append(future)
        
        # Собираем результаты
        results = [f.result() for f in ftres.as_completed(futures)]
        return sum(results)
    
# print(integrate_threaded_cython("cos", 0, math.pi / 2, n_iter=100))
# print(integrate_4("cos", 0, math.pi / 2, n_iter=100))
# print(integrate_4("math.cos", 0, math.pi / 2, n_iter=100))