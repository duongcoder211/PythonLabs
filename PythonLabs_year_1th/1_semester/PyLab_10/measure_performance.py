import timeit
from integrate_1 import integrate_1
from integrate_2 import integrate_2
from integrate_3 import integrate_3
from integrate_4 import integrate_4

rounds = [1,2,3,4]

def measure_performance():
    """Замер времени выполнения для разного числа итераций."""
    
    print("Итерации| Время (сек)")
    print("-" * 40)

    for i in rounds:
        print(f"===== Mesure integrate_{i} with function cos(x) =====")
        for n in [1000, 10000, 100000]:
            call = f"integrate_{i}(math.cos, 0, math.pi/2, n_iter={n})"

            # Замеряем время
            t = timeit.timeit(stmt=call, setup=f"import math\nfrom __main__ import integrate_{i}", number=10) / 10
            
            print(f"{n:8} | {t:.6f}")
    
    # for i in rounds:
    #     print(f"===== Mesure integrate_{i} with function x^2 =====")
    #     for n in [1000, 10000, 100000]:
    #         call = f"integrate_{i}(lambda x: x**2, 0, 1, n_iter={n})"

    #         # Замеряем время
    #         t = timeit.timeit(stmt=call, setup=f"import math\nfrom __main__ import integrate_{i}", number=10) / 10
            
    #         print(f"{n:8} | {t:.6f}")

    print("\nПримечание: время усреднено по 10 запускам")

if __name__ == "__main__":
    measure_performance()