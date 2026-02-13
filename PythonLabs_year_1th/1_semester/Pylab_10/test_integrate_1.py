import unittest
import doctest
import math
from integrate_1 import integrate_1


class TestIntegrate_1(unittest.TestCase):
    """Набор тестов для функции численного интегрирования."""
    
    def test_trigonometric_function(self):
        """Тест с тригонометрической функцией (cos)."""
        result = integrate_1(math.cos, 0, math.pi/2, n_iter=10000)         # ∫cos(x)dx от 0 до π/2 = 1
        # Проверяем с точностью 0.001 из-за численного метода
        self.assertAlmostEqual(result, 1.0, places=2, msg=f"∫cos(x)dx от 0 до π/2 должен быть ~1.0, получено {result}")
    
    def test_polynomial_function(self):
        """Тест с полиномиальной функцией (x²)."""
        result = integrate_1(lambda x: x**2, 0, 1, n_iter=10000)         # ∫x²dx от 0 до 1 = 1/3 ≈ 0.333333
        self.assertAlmostEqual(result, 1/3, places=2, msg=f"∫x²dx от 0 до 1 должен быть ~ 0.333, получено {result}")
    
    def test_iteration_count_stability(self):
        """Проверка устойчивости к изменению числа итераций."""
        # Результат должен улучшаться с увеличением итераций
        results = []
        for n in [100, 1000, 10000, 100000]:
            result = integrate_1(math.cos, 0, math.pi/2, n_iter=n)
            results.append(result)
        
        # Проверяем, что с увеличением итераций результат приближается к 1
        # (последний результат должен быть ближе к истинному значению)
        self.assertLess(abs(results[-1] - 1.0), abs(results[0] - 1.0),
                       msg="Точность должна увеличиваться с ростом итераций")
    
    def test_error_cases(self):
        """Тест обработки ошибочных входных данных."""
        with self.assertRaises(ValueError):
            integrate_1(math.cos, 5, 0, n_iter=1000)  # a > b
        
        with self.assertRaises(ValueError):
            integrate_1(math.cos, 0, 1, n_iter=0)  # n_iter <= 0
        
        with self.assertRaises(ValueError):
            integrate_1(math.cos, 0, 1, n_iter=-100)  # n_iter отрицательное
    
    def test_linear_function(self):
        """Тест с линейной функцией f(x) = x."""
        result = integrate_1(lambda x: x, 0, 1, n_iter=10000)         # ∫x dx от 0 до 1 = 0.5
        self.assertAlmostEqual(result, 0.5, places=3)
    
    def test_constant_function(self):
        """Тест с константной функцией."""
        result = integrate_1(lambda x: 5, 0, 3, n_iter=1000)         # ∫5 dx от 0 до 3 = 15
        self.assertAlmostEqual(result, 15.0, places=5)


if __name__ == "__main__":
    # Запуск doctest
    doctest.testmod(verbose=True)
    
    # Запуск unittest
    unittest.main(argv=[''], verbosity=2, exit=False)