import unittest
from function_lab_1 import searchTarget

# Тесты
class TestMath(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(searchTarget([2,7,11,15], 9), [0,1])

    def test_search_target_negative(self):
        self.assertEqual(searchTarget([3,-2,-4], -6), [1,2])

    def test_search_target_double(self):
        self.assertEqual(searchTarget([3,3], 6), [0,1])

    def test_search_target_duplicate(self):
        self.assertEqual(searchTarget([5,5,5,5,5,5,5,5], 10), [0,1])
    
    def test_search_target_zero(self):
        self.assertEqual(searchTarget([3,0,3], 6), [0,2])

    def test_search_target_empty(self):
        self.assertEqual(searchTarget([], 6), None)

    def test_search_target_one_element(self):
        self.assertEqual(searchTarget([1], 1), None)
        
# # Запуск тестов
unittest.main(argv=[''], verbosity=2, exit=False)




