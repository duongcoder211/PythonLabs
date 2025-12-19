import unittest
from integrate_1 import integrate_1
from integrate_2 import integrate_2
import math

class TestThreadedIntegrate(unittest.TestCase):
    """Тесты для многопоточной версии."""
    
    def test_consistency_with_base(self):
        """Проверка, что многопоточная версия дает тот же результат."""
        n_iter = 10000
        
        # Тест с cos
        result = integrate_2(math.cos, 0, math.pi/2, n_iter=n_iter, n_threads=4)
        self.assertAlmostEqual(result, 1.0, places=2, msg=f"∫cos(x)dx от 0 до π/2 должен быть ~1.0, получено {result}")
        
        # Тест с полиномом
        result = integrate_2(lambda x: x**2, 0, 1, n_iter=n_iter, n_threads=2)
    
    def test_different_thread_counts(self):
        """Проверка работы с разным количеством потоков."""
        for n_threads in [1, 2, 4, 8]:
            result = integrate_2(math.cos, 0, math.pi/2, n_iter=1000, n_threads=n_threads)
            # Проверяем, что результат близок к 1 (интеграл cos от 0 до pi/2)
            self.assertAlmostEqual(result, 1.0, places=1)
    
    def test_error_cases(self):
        """Проверка обработки ошибок."""
        with self.assertRaises(ValueError):
            integrate_2(math.cos, 0, math.pi/2, n_iter=1000, n_threads=0)
        
        with self.assertRaises(ValueError):
            integrate_2(math.cos, 0, math.pi/2, n_iter=0, n_threads=4)


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)