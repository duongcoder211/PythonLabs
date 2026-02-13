import math
import threading
from integrate_1 import integrate_1
from typing import Callable

# итерация 2
# оптимизация с помощью потоков

def integrate_2(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 10000, n_threads: int = 4) -> float:
    """
    Оптимизация с помощью потоков многопоточного интегрирования.
    """
    if a >= b or n_iter <= 0 or n_threads <= 0:
        raise ValueError("Invalid parameters")
    
    results = [0.0] * n_threads
    threads = []
    step = (b - a) / n_iter
    chunk_size = n_iter // n_threads
    
    def worker(thread_id: int, start_idx: int, end_idx: int):
        acc = 0.0
        for i in range(start_idx, end_idx):
            acc += f(a + i * step) * step
        results[thread_id] = acc
    
    for i in range(n_threads):
        start_idx = i * chunk_size
        end_idx = n_iter if i == n_threads - 1 else start_idx + chunk_size
        
        t = threading.Thread(target=worker, args=(i, start_idx, end_idx))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    return sum(results)

# integrate_2(math.cos, 0, math.pi / 2, n_iter=100)

# print(integrate_2(math.sin, 0, math.pi, n_iter=10000))


def benchmark_threads():
    """Сравнение производительности разного количества потоков"""
    import time
    
    n_iter = 1000000  # Большое количество итераций для наглядности
    test_cases = [
        ("cos", math.cos, 0, math.pi/2),
        ("x^2", lambda x: x**2, 0, 1),
    ]
    
    results = {}
    
    for name, func, a, b in test_cases:
        print(f"\nТестирование функции: {name + "(x)" if name == "cos" else name}")
        print("-" * 50)
        
        # Тестируем разное количество потоков
        for n_threads in [1, 2, 4, 8]:
            # Многопоточный вариант
            start = time.time()
            result_threaded = integrate_2(func, a, b, n_iter=n_iter, n_threads=n_threads)
            threaded_time = time.time() - start
            
            print(f"Потоков: {n_threads:2d} | "f"Время: {threaded_time:.4f} секунд")

# benchmark_threads()