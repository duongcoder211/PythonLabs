import unittest
import math
from integrate_3 import integrate_3
from integrate_2 import integrate_2

def square_func(x):
    return x**2

class TestIntegrate3(unittest.TestCase):
    """Тесты для функции integrate_3 (ProcessPoolExecutor)."""
    
    def test_basic_functionality(self):
        """Тест базовой функциональности с sin(x)."""
        result = integrate_3(math.sin, 0, math.pi, n_jobs=2, n_iter=10000)
        # ∫sin(x)dx от 0 до π = 2
        self.assertAlmostEqual(result, 2.0, places=1)
    
    def test_cos_function(self):
        """Тест с cos(x) от 0 до π/2."""
        result = integrate_3(math.cos, 0, math.pi/2, n_jobs=2, n_iter=10000)
        # ∫cos(x)dx от 0 до π/2 = 1
        self.assertAlmostEqual(result, 1.0, places=1)
    
    def test_polynomial_function(self):
        """Тест с полиномиальной функцией x²."""
        result = integrate_3(square_func, 0, 1, n_jobs=2, n_iter=10000)
        # ∫x²dx от 0 до 1 = 1/3 ≈ 0.333333
        self.assertAlmostEqual(result, 1/3, places=2)
    
    def test_different_number_of_workers(self):
        """Тест работы с разным количеством процессов."""
        n_iter = 100000
        results = []
        
        for n_jobs in [1, 2, 4]:
            result = integrate_3(math.cos, 0, math.pi/2, n_jobs=n_jobs, n_iter=n_iter)
            results.append(result)
            # Проверяем, что результат приблизительно правильный
            self.assertAlmostEqual(result, 1.0, places=1)
        
        # Проверяем, что все результаты приблизительно одинаковы
        # (разные процессы должны давать одинаковый результат)
        for i in range(1, len(results)):
            self.assertAlmostEqual(results[i], results[0], places=5)
    
    def test_error_a_greater_than_b(self):
        """Тест обработки ошибки при a >= b."""
        with self.assertRaises(ValueError):
            integrate_3(math.cos, 5, 0, n_jobs=2, n_iter=1000)
    
    def test_error_zero_iterations(self):
        """Тест обработки ошибки при n_iter = 0."""
        with self.assertRaises(ValueError):
            integrate_3(math.cos, 0, 1, n_jobs=2, n_iter=0)
    
    def test_error_negative_iterations(self):
        """Тест обработки ошибки при отрицательном n_iter."""
        with self.assertRaises(ValueError):
            integrate_3(math.cos, 0, 1, n_jobs=2, n_iter=-100)
    
    def test_error_zero_jobs(self):
        """Тест обработки ошибки при n_jobs = 0."""
        with self.assertRaises(ValueError):
            integrate_3(math.cos, 0, 1, n_jobs=0, n_iter=1000)
    
    def test_error_negative_jobs(self):
        """Тест обработки ошибки при отрицательном n_jobs."""
        with self.assertRaises(ValueError):
            integrate_3(math.cos, 0, 1, n_jobs=-2, n_iter=1000)
    
    def test_consistency_with_sequential_version(self):
        """Проверка согласованности с последовательной версией."""
        n_iter = 100000
        
        # Результат от ProcessPoolExecutor
        result_parallel = integrate_3(math.cos, 0, math.pi/2, n_jobs=4, n_iter=n_iter)
        
        # Результат от последовательной версии
        result_sequential = integrate_2(math.cos, 0, math.pi/2, n_iter=n_iter)
        
        # Они должны быть очень близки
        self.assertAlmostEqual(result_parallel, result_sequential, places=8)

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)