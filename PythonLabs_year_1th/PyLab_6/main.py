import matplotlib.pyplot as plt
import random

from benchmark import benchmark
from gen_bin_tree_recursive import gen_bin_tree_recursive
from gen_bin_tree_optimized_recursive import gen_bin_tree_optimized_recursive
from gen_bin_tree_iterative import gen_bin_tree_iterative
from gen_bin_tree_optimized_iterative import gen_bin_tree_optimized_iterative

def main():
    """
      Вычисление среднего времени создания бинарого дерева по рекусцией и итеруемому способу, так же без оптимизации и с оптимизацией (lru_cache)
      А затем строение диаграмм сравнения 4 случая с помощью модули matplotlib.pyplot
        - Сравнение lru_cache РекФакт и НРекФакт
        - Сравнение n/a optimization РекФакт и НРекФакт
        - Сравнение РекФакт (lru_cache) и РекФакт n/a optimization
        - Сравнение НРекФакт (lru_cache) и НРекФакт n/a optimization
    """
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(1,11,1))

    res_recursive = []
    res_iterative = []
    res_optimized_recursive = []
    res_optimized_iterative = []

    for n in test_data:
      res_recursive.append(benchmark(gen_bin_tree_recursive, n, number=1000, repeat=5))
      res_iterative.append(benchmark(gen_bin_tree_iterative, n, number=1000, repeat=5))
      res_optimized_recursive.append(benchmark(gen_bin_tree_optimized_recursive, n, number=1000, repeat=5))
      res_optimized_iterative.append(benchmark(gen_bin_tree_optimized_iterative, n, number=1000, repeat=5))
    
    # Визуализация
    fig, axs = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Сравнение рекурсивной и итеративной генерации бинарного дерева\n(при root = 6)")

    axs[0, 0].plot(test_data, res_recursive, label="Рекурсивный")
    axs[0, 0].plot(test_data, res_iterative, label="Итеративный")
    axs[0, 0].set_title("Сравнение РекДерева без lru_cache и ИтерДерева без lru_cache")
    axs[0, 0].set_xlabel("height")
    axs[0, 0].set_ylabel("time (s)")
    axs[0, 0].legend()

    axs[0, 1].plot(test_data, res_optimized_recursive, label="Рекурсивный")
    axs[0, 1].plot(test_data, res_optimized_iterative, label="Итеративный")
    axs[0, 1].set_title("Сравнение РекДерева с lru_cache и ИтерДерева с lru_cache")
    axs[0, 1].set_xlabel("height")
    axs[0, 1].set_ylabel("time (s)")
    axs[0, 1].legend()

    axs[1, 0].plot(test_data, res_recursive, label="без lru_cache")
    axs[1, 0].plot(test_data, res_optimized_recursive, label="с lru_cache")
    axs[1, 0].set_title("Сравнение РекДерева без lru_cache и РекДерева с lru_cache")
    axs[1, 0].set_xlabel("height")
    axs[1, 0].set_ylabel("time (s)")
    axs[1, 0].legend()

    axs[1, 1].plot(test_data, res_iterative, label="без lru_cache")
    axs[1, 1].plot(test_data, res_optimized_iterative, label="с lru_cache")
    axs[1, 1].set_title("Сравнение РекДерева без lru_cache и ИтерДерева с lru_cache")
    axs[1, 1].set_xlabel("height")
    axs[1, 1].set_ylabel("time (s)")
    axs[1, 1].legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()




