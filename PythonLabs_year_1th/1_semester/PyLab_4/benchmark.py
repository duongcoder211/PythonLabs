import timeit

def benchmark(func, num, number=1, repeat=5):
    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(num), number=number, repeat=repeat)
    return sum(times)/len(times)
