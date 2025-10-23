import timeit

def benchmark(func, height, number=1, repeat=5):
    """Возвращает среднее время выполнения func(h, r)"""
    times = timeit.repeat(lambda: func(height, root = 10), number=number, repeat=repeat)
    return sum(times)/len(times)
