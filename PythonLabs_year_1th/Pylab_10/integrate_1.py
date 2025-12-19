import math
import timeit
from typing import Callable, Optional

# итерация 1
# def intergrate_1(f, a, b, *, n_iter=1000):
#   """
#   - написать документацию для функции
#   - аннотировать переменные
#   - написать тесты для функции (2 штуки тут)
#   - + тесты с помощью Unittest
#   >>> round(integrate_1(math.cos, 0, math.pi / 2, n_iter=100), 5)
#   1.00783
#   - замерить время вычисления функции (timeit), записать время
#   вычисления
#   """
#   acc = 0
#   step = (b - a) / n_iter
#   for i in range(n_iter):
#     acc += f(a + i*step) * step
#   return acc

# intergrate_1(math.cos, 0, math.pi / 2, n_iter=100)
# print(intergrate_1(math.sin, 0, math.pi))


def integrate_1(f: Callable[[float], float], a: float, b: float, *, n_iter: Optional[int] = 10000) -> float:
    """
    Вычисляет определенный интеграл функции методом правых прямоугольников.
    
    Метод прямоугольников — простейший метод численного интегрирования,
    который аппроксимирует площадь под кривой как сумму площадей прямоугольников.
    Используется правосторонняя формула (right Riemann sum).
    
    Parameters
    ----------
    f : Callable[[float], float]
        Интегрируемая функция одного аргумента. Должна принимать число и возвращать число.
    a : float
        Нижний предел интегрирования.
    b : float
        Верхний предел интегрирования.
    n_iter : int, optional
        Количество подотрезков разбиения (по умолчанию 10000).
        Большее значение повышает точность, но увеличивает время вычислений.
    
    Returns
    -------
    float
        Приближенное значение определенного интеграла ∫[a,b] f(x) dx.
    
    Raises
    ------
    ValueError
        Если a >= b или n_iter <= 0.
    
    Notes
    -----
    Точность метода: O(1/n_iter).
    Не рекомендуется для функций с быстрыми осцилляциями или разрывами.
    
    Examples
    --------
    Пример с тригонометрической функцией:
    >>> integrate(math.cos, 0, math.pi/2, n_iter=10000)
    1.0
    
    Пример с полиномиальной функцией:
    >>> integrate(lambda x: x**2, 0, 1, n_iter=10000)
    0.333...
    
    >>> import math
    >>> round(integrate(math.cos, 0, math.pi / 2, n_iter=100), 5)
    1.00783
    """
    if a >= b:
        raise ValueError("a must be less than b")
    if n_iter <= 0:
        raise ValueError("n_iter must be positive")
    
    acc = 0.0
    step = (b - a) / n_iter
    
    for i in range(n_iter):
        acc += f(a + i * step) * step
    
    return acc

# print(integrate_1(math.cos, 0, math.pi / 2, n_iter=100))
# print(integrate_1(math.sin, 0, math.pi))

# def measure_performance():
#     """Замер времени выполнения для разного числа итераций."""
    
#     print("Итерации| Время (сек)")
#     print("-" * 40)

#     for n in [1000, 10000, 100000]:
#         call = f"integrate_1(math.cos, 0, math.pi/2, n_iter={n})"

#         # Замеряем время
#         t = timeit.timeit(stmt=call, setup="import math\nfrom __main__  import integrate_1", number=10) / 10
        
#         print(f"{n:8} | {t:.6f}")
    
#     for n in [1000, 10000, 100000]:
#         call = f"integrate_1(lambda x: x**2, 0, 1, n_iter={n})"

#         # Замеряем время
#         t = timeit.timeit(stmt=call, setup="import math\nfrom __main__  import integrate_1", number=10) / 10
        
#         print(f"{n:8} | {t:.6f}")

#     print("\nПримечание: время усреднено по 10 запускам")

# # measure_performance()