import unittest
from guess_number import guess_number

# Тесты
class TestMath(unittest.TestCase):
    def test_guess_number_positive(self):
        self.assertEqual(guess_number(1,[2,7,11,15], "bin"), None)

    def test_guess_number_negative(self):
        self.assertEqual(guess_number(3, [3,-2,-4]), [3, 3])

    def test_guess_number_double(self):
        self.assertEqual(guess_number(4, [3,3]), None)

    def test_guess_number_duplicate(self):
        self.assertEqual(guess_number(5, [5,5,5,5,5,5,5,5]), [5,5])
    
    def test_guess_number_zero(self):
        self.assertEqual(guess_number(6, [3,0,3], "bin"), None)

    def test_guess_number_empty(self):
        self.assertEqual(guess_number(7, []), None)

    def test_guess_number_one_element(self):
        self.assertEqual(guess_number(8, [8]), [8,8])
        
# # Запуск тестов
unittest.main(argv=[''], verbosity=2, exit=False)




