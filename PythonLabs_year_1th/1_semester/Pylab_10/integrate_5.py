import math

# итерация 5

# переписать код функции integrate с использование noGIL.
# сделать замеры позволяющие оценить время выполнения кода с 2, 4, 6 потоками и сравнить
# время вычисления с помощью потоков integrate  без GIL (noGIL ) и сайтонизированной с
# временем вычисления с помощью процессов сайтонизированной версии


# * - оценить возможность применения примитивов синхронизации (семафор, мьютекс), дать
# объяснение имеет ли это смысл или нет и почему?

# * - python 3.14 исследовать изменяются ли значения времени вычисления , произведенные
# в итерации 2 (если мы используем 3.14, нужно ли нам отпускать GIL)

# integrate_5_nogil_benchmark.py (исправленная версия)
import math
import time
import threading
import concurrent.futures as ftres
import multiprocessing as mp
from typing import List, Dict, Tuple
import sys
import os

# Импортируем Cython модули
try:
    from integrate_5_cy import integrate_nogil, integrate_openmp
    CYTHON_AVAILABLE = True
except ImportError as e:
    print(f"Cython модуль не доступен: {e}")
    print("Скомпилируйте с помощью: python setup_5.py build_ext --inplace")
    CYTHON_AVAILABLE = False

# ============================================================================
# Глобальные функции для использования в процессах
# (должны быть определены на верхнем уровне, не внутри других функций)
# ============================================================================

def worker_integrate(args):
    """
    Глобальная функция-рабочий для использования в процессах.
    Должна быть на верхнем уровне для правильной сериализации в Windows.
    """
    i, func_name, a_val, step_val, chunk_iter = args
    a_i = a_val + i * step_val
    b_i = a_val + (i + 1) * step_val
    return integrate_nogil(func_name, a_i, b_i, chunk_iter)


def worker_integrate_simple(func_name, a_i, b_i, chunk_iter):
    """
    Альтернативная глобальная функция для использования в ThreadPoolExecutor.
    """
    return integrate_nogil(func_name, a_i, b_i, chunk_iter)


# ============================================================================
# Многопоточные версии с разными подходами
# ============================================================================

class ThreadSafeAccumulator:
    """Потокобезопасный аккумулятор для демонстрации синхронизации."""
    
    def __init__(self):
        self._value = 0.0
        self._lock = threading.Lock()
    
    def add(self, value: float):
        """Добавить значение с использованием мьютекса."""
        with self._lock:
            self._value += value
    
    def get_value(self) -> float:
        """Получить текущее значение."""
        with self._lock:
            return self._value


def integrate_threads_simple(func_name: str,
                            a: float,
                            b: float,
                            n_iter: int = 1000000,
                            n_threads: int = 4) -> float:
    """
    Простая многопоточная версия с использованием threading.
    """
    if not CYTHON_AVAILABLE:
        raise RuntimeError("Cython module not available")
    
    chunk_iter = n_iter // n_threads
    step = (b - a) / n_threads
    results = [0.0] * n_threads
    threads = []
    
    def worker(thread_id: int, a_i: float, b_i: float):
        """Функция, выполняемая в каждом потоке."""
        results[thread_id] = integrate_nogil(func_name, a_i, b_i, chunk_iter)
    
    for i in range(n_threads):
        a_i = a + i * step
        b_i = a + (i + 1) * step if i < n_threads - 1 else b
        thread = threading.Thread(target=worker, args=(i, a_i, b_i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return sum(results)


def integrate_threads_with_sync(func_name: str,
                               a: float,
                               b: float,
                               n_iter: int = 1000000,
                               n_threads: int = 4) -> float:
    """
    Многопоточная версия с синхронизацией (демонстрация мьютекса).
    """
    if not CYTHON_AVAILABLE:
        raise RuntimeError("Cython module not available")
    
    chunk_iter = n_iter // n_threads
    step = (b - a) / n_threads
    accumulator = ThreadSafeAccumulator()
    threads = []
    
    def worker(a_i: float, b_i: float):
        """Функция с использованием синхронизации."""
        result = integrate_nogil(func_name, a_i, b_i, chunk_iter)
        accumulator.add(result)
    
    for i in range(n_threads):
        a_i = a + i * step
        b_i = a + (i + 1) * step if i < n_threads - 1 else b
        thread = threading.Thread(target=worker, args=(a_i, b_i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return accumulator.get_value()


def integrate_threads_concurrent(func_name: str,
                                a: float,
                                b: float,
                                n_iter: int = 1000000,
                                n_threads: int = 4) -> float:
    """
    Многопоточная версия с использованием concurrent.futures.
    """
    if not CYTHON_AVAILABLE:
        raise RuntimeError("Cython module not available")
    
    chunk_iter = n_iter // n_threads
    step = (b - a) / n_threads
    
    with ftres.ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = []
        for i in range(n_threads):
            a_i = a + i * step
            b_i = a + (i + 1) * step if i < n_threads - 1 else b
            # Используем глобальную функцию
            futures.append(executor.submit(worker_integrate_simple, func_name, a_i, b_i, chunk_iter))
        
        results = [f.result() for f in ftres.as_completed(futures)]
        return sum(results)


# ============================================================================
# Многопроцессные версии
# ============================================================================

def integrate_processes(func_name: str,
                       a: float,
                       b: float,
                       n_iter: int = 1000000,
                       n_processes: int = 4) -> float:
    """
    Многопроцессная версия для сравнения.
    """
    if not CYTHON_AVAILABLE:
        raise RuntimeError("Cython module not available")
    
    chunk_iter = n_iter // n_processes
    step = (b - a) / n_processes
    args_list = [(i, func_name, a, step, chunk_iter) 
                 for i in range(n_processes)]
    
    with mp.Pool(processes=n_processes) as pool:
        results = pool.map(worker_integrate, args_list)
    
    return sum(results)


# Упрощенная версия без использования класса Pool
def integrate_processes_simple(func_name: str,
                              a: float,
                              b: float,
                              n_iter: int = 1000000,
                              n_processes: int = 4) -> float:
    """
    Упрощенная многопроцессная версия с использованием Process и очереди.
    """
    if not CYTHON_AVAILABLE:
        raise RuntimeError("Cython module not available")
    
    chunk_iter = n_iter // n_processes
    step = (b - a) / n_processes
    
    processes = []
    results_queue = mp.Queue()
    
    def process_worker(worker_id, func_name, a_i, b_i, chunk_iter, queue):
        """Функция для процесса."""
        result = integrate_nogil(func_name, a_i, b_i, chunk_iter)
        queue.put((worker_id, result))
    
    for i in range(n_processes):
        a_i = a + i * step
        b_i = a + (i + 1) * step if i < n_processes - 1 else b
        
        process = mp.Process(
            target=process_worker,
            args=(i, func_name, a_i, b_i, chunk_iter, results_queue)
        )
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    # Собираем результаты
    results = []
    while not results_queue.empty():
        results.append(results_queue.get()[1])
    
    return sum(results)


# ============================================================================
# Бенчмарки и сравнение производительности
# ============================================================================

def benchmark_nogil_vs_processes():
    """
    Сравнение производительности многопоточных (с noGIL) и многопроцессных версий.
    """
    if not CYTHON_AVAILABLE:
        print("Cython не доступен, пропускаем тест...")
        return
    
    print("\n" + "="*80)
    print("БЕНЧМАРК: ПОТОКИ с noGIL vs ПРОЦЕССЫ")
    print("="*80)
    
    func_name = "cos"
    a, b = 0, math.pi/2
    n_iter = 2000000
    
    print(f"Функция: {func_name}, n_iter={n_iter:,}")
    print("-"*80)
    print(f"{'Метод':<30} {'Работники':<10} {'Время (с)':<12} {'Ускорение':<10} {'Эффективность':<12}")
    print("-"*80)
    
    # Базовая однопоточная версия
    start = time.perf_counter()
    result_base = integrate_nogil(func_name, a, b, n_iter)
    time_base = time.perf_counter() - start
    print(f"{'noGIL (1 поток)':<30} {'1':<10} {time_base:<12.4f} {'1.00x':<10} {'100%':<12}")
    
    # Тестируем разное количество потоков
    for n_workers in [2, 4, 6, 8]:
        try:
            # Многопоточная версия (simple)
            start = time.perf_counter()
            result_threads = integrate_threads_simple(func_name, a, b, n_iter, n_workers)
            time_threads = time.perf_counter() - start
            speedup_threads = time_base / time_threads
            efficiency_threads = (speedup_threads / n_workers) * 100
            
            # Многопроцессная версия
            start = time.perf_counter()
            result_processes = integrate_processes(func_name, a, b, n_iter, n_workers)
            time_processes = time.perf_counter() - start
            speedup_processes = time_base / time_processes
            efficiency_processes = (speedup_processes / n_workers) * 100
            
            print(f"{'Потоки (noGIL)':<30} {n_workers:<10} {time_threads:<12.4f} "
                  f"{speedup_threads:<10.2f}x {efficiency_threads:<10.1f}%")
            print(f"{'Процессы':<30} {n_workers:<10} {time_processes:<12.4f} "
                  f"{speedup_processes:<10.2f}x {efficiency_processes:<10.1f}%")
            
            if time_processes > 0 and time_threads > 0:
                print(f"{'Отношение (П/П)':<30} {n_workers:<10} {time_threads/time_processes:<12.2f} "
                      f"{speedup_threads/speedup_processes:<10.2f}x "
                      f"{efficiency_threads/efficiency_processes:<10.1f}%")
            
            print("-"*80)
            
        except Exception as e:
            print(f"Ошибка при тестировании с {n_workers} работниками: {e}")
            print("-"*80)
    
    # Тест OpenMP (если доступно)
    try:
        start = time.perf_counter()
        result_openmp = integrate_openmp(func_name, a, b, n_iter)
        time_openmp = time.perf_counter() - start
        speedup_openmp = time_base / time_openmp
        
        print(f"{'OpenMP (авто)':<30} {'auto':<10} {time_openmp:<12.4f} "
              f"{speedup_openmp:<10.2f}x {'-':<12}")
    except Exception as e:
        print(f"OpenMP не доступен: {e}")


def main():
    """
    Основная функция.
    """
    print("Итерация 5: Использование noGIL в Cython")
    print("="*80)
    
    if not CYTHON_AVAILABLE:
        print("Cython модуль не доступен!")
        print("Для компиляции выполните:")
        print("  1. Установите Cython: pip install cython")
        print("  2. Скомпилируйте: python setup_5.py build_ext --inplace")
        print("  3. Запустите скрипт заново")
        return
    
    print(f"Платформа: {sys.platform}")
    print(f"Количество ядер CPU: {os.cpu_count()}")
    
    # Запускаем тесты
    benchmark_nogil_vs_processes()


if __name__ == "__main__":
    # Для многопроцессности в Windows
    if sys.platform == "win32":
        mp.freeze_support()
    
    main()
    # print(integrate_threads_simple("cos", 0, 1, n_iter=1000, n_threads=4))

# integrate_1(math.cos, 0, math.pi / 2, n_iter=100)

# print(integrate(math.sin, 0, math.pi))