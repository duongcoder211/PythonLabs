import matplotlib.pyplot as plt
import random

from benchmark import benchmark
from fact_recursive import fact_recursive
from fact_iterative import fact_iterative

def main():
    """
      Вычисление среднего времени выполнения 2 подхода поиска факториала (recursive, iterative) 
      А затем создание графика сравнение времени выполнения каждого подхода
    """
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(1, 300, 10))

    res_recursive = []
    res_iterative = []

    for n in test_data:
      res_recursive.append(benchmark(fact_recursive, n, number=1000, repeat=5))
      res_iterative.append(benchmark(fact_iterative, n, number=1000, repeat=5))
    
    # Визуализация
    plt.plot(test_data, res_recursive, label="Recursive")
    plt.plot(test_data, res_iterative, label="Iterative")
    plt.title("Сравнение рекурсивного и итеративного факториала")
    plt.xlabel("n")
    plt.ylabel("time (s)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
