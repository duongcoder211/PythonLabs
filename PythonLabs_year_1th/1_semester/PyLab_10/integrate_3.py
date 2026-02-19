import math
from typing import Callable
import concurrent.futures as ftres
from functools import partial
from integrate_2 import integrate_2

# итерация 3
# оптимизация с помощью процессов

def integrate_3(f: Callable[[float], float], a: float, b: float, *, n_jobs: int = 2, n_iter: int = 1000) -> float:
    """
    Вычисление интеграла с использованием ProcessPoolExecutor (процессы).
    
    Parameters
    ----------
    f : Callable[[float], float]
        Интегрируемая функция.
    a, b : float
        Нижний и верхний пределы интегрирования.
    n_jobs : int, optional
        Количество процессов (по умолчанию 2).
    n_iter : int, optional
        Общее количество итераций (по умолчанию 1000).
    
    Return
    ------
    float
        Приближенное значение интеграла.
    """
    if a >= b:
        raise ValueError("a must be less than b")
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")
    if n_jobs <= 0:
        raise ValueError("n_jobs must be positive")
    
    # Создаем пул процессов
    with ftres.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        # Делаем n_iter кратным n_jobs
        chunk_iter = n_iter // n_jobs
        
        # Создаем partial функцию с фиксированными параметрами
        spawn = partial(executor.submit, integrate_2, f, n_iter=chunk_iter)
        
        # Вычисляем шаг для разделения интервала
        step = (b - a) / n_jobs
        
        # Создаем задачи для каждого процесса
        fs = [spawn(a + i * step, a + (i + 1) * step) 
              for i in range(n_jobs)]
        
        # Собираем результаты по мере завершения
        results = [f.result() for f in ftres.as_completed(fs)]
        
        return sum(results)
    
# if __name__ == '__main__':
#   print(integrate_3(math.cos, 0, math.pi / 2, n_jobs=2, n_iter=1000))

# if __name__ == '__main__':
#   print(integrate_3(math.sin, 0, math.pi))


def compare_performance():
    """
    Детальное сравнение производительности с разным количеством итераций.
    """
    import time
    from integrate_1 import integrate_1
    from integrate_2 import integrate_2
    from integrate_async import integrate_async
    print("\n" + "=" * 70)
    print("ДЕТАЛЬНОЕ СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 70)
    
    func = math.cos
    a, b = 0, math.pi/2
    
    # Разные объемы вычислений
    test_iterations = [10000, 50000, 100000, 500000, 1000000]
    
    results = []
    
    for n_iter in test_iterations:
        print(f"\nКоличество итераций: {n_iter:,}")
        print("-" * 50)
        
        # Базовый метод
        start = time.time()
        result_base = integrate_1(func, a, b, n_iter=n_iter)
        time_base = time.time() - start
        
        row = {
            'n_iter': n_iter,
            'base_time': time_base,
            'base_result': result_base
        }
        
        # Тестируем для разного количества работников
        for n_workers in [2, 4, 6, 8]:
            # Threads
            start = time.time()
            result_thread = integrate_async(func, a, b, n_jobs=n_workers, n_iter=n_iter)
            time_thread = time.time() - start
            
            # Processes
            start = time.time()
            result_process = integrate_3(func, a, b, n_jobs=n_workers, n_iter=n_iter)
            time_process = time.time() - start
            
            # Сохраняем результаты
            row[f'thread_{n_workers}_time'] = time_thread
            row[f'process_{n_workers}_time'] = time_process
            row[f'thread_{n_workers}_speedup'] = time_base / time_thread if time_thread > 0 else 0
            row[f'process_{n_workers}_speedup'] = time_base / time_process if time_process > 0 else 0
            
            print(f"{'Workers':<10} {n_workers:<4} | "
                  f"{'Threads:':<8} {time_thread:<8.4f}s ({row[f'thread_{n_workers}_speedup']:.2f}x) | "
                  f"{'Processes:':<10} {time_process:<8.4f}s ({row[f'process_{n_workers}_speedup']:.2f}x)")
        
        results.append(row)
    
    # Анализ результатов
    print("\n" + "=" * 70)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("=" * 70)
    
    print("\nРекомендации по выбору метода:")
    print("-" * 40)
    
    for row in results:
        n_iter = row['n_iter']
        
        # Находим лучший метод
        best_time = row['base_time']
        best_method = "Базовый"
        
        for n_workers in [2, 4, 6, 8]:
            if row[f'thread_{n_workers}_time'] < best_time:
                best_time = row[f'thread_{n_workers}_time']
                best_method = f"ThreadPool ({n_workers} workers)"
            
            if row[f'process_{n_workers}_time'] < best_time:
                best_time = row[f'process_{n_workers}_time']
                best_method = f"ProcessPool ({n_workers} workers)"
        
        print(f"При n_iter={n_iter:,}: {best_method} (время: {best_time:.4f}s)")
        
        # Выводим, когда процессы начинают быть эффективнее потоков
        if n_iter > 100000:
            thread_4_speedup = row.get('thread_4_speedup', 0)
            process_4_speedup = row.get('process_4_speedup', 0)
            
            if process_4_speedup > thread_4_speedup * 1.5:
                print(f"  => ProcessPool значительно быстрее ThreadPool ({process_4_speedup:.2f}x vs {thread_4_speedup:.2f}x)")
            elif thread_4_speedup > process_4_speedup:
                print(f"  => ThreadPool быстрее ProcessPool ({thread_4_speedup:.2f}x vs {process_4_speedup:.2f}x)")

# if __name__ == "__main__":
#   compare_performance()