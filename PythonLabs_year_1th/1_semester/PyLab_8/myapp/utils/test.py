import unittest
from models import *
from unittest.mock import Mock
from controllers import SimpleHTTPRequestHandler
from utils.currencies_api import get_currencies
from io import BytesIO

class TestModels(unittest.TestCase):
    def setUp(self):
        self.author = Author("Dao Manh Duong", "P3121")
        self.app = App("My first project", "1.0.0 Beta", self.author)
        self.currency = Currency("R724", "892", "USD", "Dollars", 93.3953, 1000)
        self.user = User(471893, "Bla Bla Bla")
        self.user_currency = UserCurrency(1, self.user.id, self.currency.id)

    def test_app_with_valid_parameters(self):
        """Тест объявления модели App"""
        self.assertEqual(self.app.name, "My first project")
        self.assertEqual(self.app.version, "1.0.0 Beta")
        self.assertEqual(self.app.author, self.author)
        # assert app.name == "My first project"
        # assert app.version == "1.0.0 Beta"
        # assert app.author == author

    def test_app_with_invalid_parameters(self):
        """Test объявляется с неправильным параметром App"""
        self.assertRaises(TypeError, App, name="MyApp", version="1.0.0", author=self.currency)
        self.assertRaises(TypeError, App, name="MyApp", version=1.0, author=self.author)
        self.assertRaises(TypeError, App, name=12345, version="1.0.0", author=self.author)

        # with self.assertRaises(TypeError): #dont use this test method because
        #     print("start")
        #     Author(name=1234, group="P3121") #if this test PASS then next test is NOT executed
        #     Author(name="Author Name", group=7483) # this test NOT executed if previous test passed
        #     print("stop") # this print() is NOT executed if previous test passed

    def test_author_with_valid_parameters(self):
        """Тест объявления модели Author"""
        self.assertEqual(self.author.name, "Dao Manh Duong")
        self.assertEqual(self.author.group, "P3121")

    def test_author_with_invalid_parameters(self):
        """Test объявляется с неправильным параметром Author"""
        self.assertRaises(TypeError, Author, name=1234, group="P3121")
        self.assertRaises(TypeError, Author, name="Author Name", group=7483)
        self.assertRaises(TypeError, Author, "D", "P3121") #Name must be of type str at least 2 characters

    def test_user_with_valid_parameters(self):
        """Тест объявления модели User"""
        self.assertEqual(self.user.id, 471893)
        self.assertEqual(self.user.name, "Bla Bla Bla")

    def test_user_with_invalid_parameters(self):
        """Test объявляется с неправильным параметром User"""
        self.assertRaises(TypeError, User, id_="1234", name="User of id 1234") #id must be an integer greater than or equal to zero
        self.assertRaises(TypeError, User, id_=-99, name="User of id 1234") #id must be an integer greater than or equal to zero
        self.assertRaises(TypeError, User, id_=9.374, name="User of id 1234") #id must be an integer greater than or equal to zero
        self.assertRaises(TypeError, User, id_="1234", name="U") #name length must be <= 30
        self.assertRaises(TypeError, User, id_="1234", name="U"*31) #name must be str
        self.assertRaises(TypeError, User, id_=1234, name=" 1User number 1") #name must be start with letter

    def test_currency_with_valid_parameters(self):
        """Тест объявления модели Currency"""
        self.assertEqual(self.currency.id, "R724")
        self.assertEqual(self.currency.num_code, "892")
        self.assertEqual(self.currency.char_code, "USD")
        self.assertEqual(self.currency.name, "Dollars")
        self.assertEqual(self.currency.value, 93.3953)
        self.assertEqual(self.currency.nominal, 1000)

    def test_currency_with_invalid_parameters(self):
        """Test объявляется с неправильным параметром Currency"""
        self.assertRaises(TypeError, Currency, id_=-999, num_code="892", char_code="USD", name="Dollars", value=93.3953, nominal=1000) #id must be a nonempty string start with a letter
        self.assertRaises(TypeError, Currency, id_=724.999, num_code="892", char_code="USD", name="Dollars", value=93.3953, nominal=1000)
        self.assertRaises(TypeError, Currency, id_="724", num_code="892", char_code="USD", name="Dollars", value=93.3953, nominal=1000)
        self.assertRaises(TypeError, Currency, id_=724, num_code=888, char_code="USD", name="Dollars", value=93.3953, nominal=1000) #num_code must be an string
        self.assertRaises(TypeError, Currency, id_=724, num_code="892", char_code=444, name="Dollars", value=93.3953, nominal=1000) #char_code must be a string of letters
        self.assertRaises(TypeError, Currency, id_=724, num_code="892", char_code="444", name="Dollars", value=93.3953, nominal=1000)
        self.assertRaises(TypeError, Currency, id_=724, num_code="892", char_code="USD", name=99999, value=93.3953, nominal=1000) #name must be a string length not of None and at most 50 characters long
        self.assertRaises(TypeError, Currency, id_=724, num_code="892", char_code="USD", name=None, value=93.3953, nominal=1000)
        self.assertRaises(TypeError, Currency, id_=724, num_code="892", char_code="USD", name="N"*51, value=93.3953, nominal=1000)
        self.assertRaises(TypeError, Currency, id_=724, num_code="892", char_code="USD", name="Dollars", value=-45354, nominal=1000) #value must be a number greater than zero
        self.assertRaises(TypeError, Currency, id_=724, num_code="892", char_code="USD", name="Dollars", value="45354", nominal=1000)
        self.assertRaises(TypeError, Currency, id_=724, num_code="892", char_code="USD", name="Dollars", value="45354", nominal=-999) #nominal must be an integer greater than or equal to zero
        self.assertRaises(TypeError, Currency, id_=724, num_code="892", char_code="USD", name="Dollars", value="45354", nominal=1000.1111)
        self.assertRaises(TypeError, Currency, id_=724, num_code="892", char_code="USD", name="Dollars", value="45354", nominal="1000")

    def test_user_currency_with_valid_parameters(self):
        """Тест объявления модели UserCurrency"""
        self.assertEqual(self.user_currency.id, 1)
        self.assertEqual(self.user.id, 471893)
        self.assertEqual(self.currency.id, "R724")

    def test_user_currency_with_invalid_parameters(self):
        """Test объявляется с неправильным параметром UserCurrency"""
        self.assertRaises(TypeError, UserCurrency, id_="1234", user_id=123, currency_id=345) #id must be an integer greater than or equal to 0
        self.assertRaises(TypeError, UserCurrency, id_=-999, user_id=123, currency_id=345)
        self.assertRaises(TypeError, UserCurrency, id_=98.999, user_id=123, currency_id=345)
        self.assertRaises(TypeError, UserCurrency, id_=1234, user_id=-123, currency_id=345) #user id must be an integer greater than or equal to 0
        self.assertRaises(TypeError, UserCurrency, id_=1234, user_id="123", currency_id=345)
        self.assertRaises(TypeError, UserCurrency, id_=1234, user_id=-123.999, currency_id=345)
        self.assertRaises(TypeError, UserCurrency, id_=1234, user_id=123, currency_id=-345) #currency id must be a nonempty string start with a letter
        self.assertRaises(TypeError, UserCurrency, id_=1234, user_id=123, currency_id=345.345)
        self.assertRaises(TypeError, UserCurrency, id_=1234, user_id=123, currency_id="345")
        self.assertRaises(TypeError, UserCurrency, id_=1234, user_id=123, currency_id="")


class TestSimpleHTTPRequestHandler(unittest.TestCase):
    def setUp(self):
        self.mock_request = Mock()

        # Создание BytesIO, содержающее реальное HTTP request
        request_data = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
        self.request_file = BytesIO(request_data)
        # Mock makefile для возвращения file-like object
        self.mock_request.makefile.return_value = self.request_file
        self.mock_client_address = ('127.0.0.1', 8080)
        self.mock_server = Mock()

        self.controller = SimpleHTTPRequestHandler(self.mock_request, self.mock_client_address, self.mock_server)

    def test_initialization(self):
        self.assertEqual(self.controller.main_author.name, 'Dao Manh Duong')
        self.assertEqual(self.controller.main_app.name, 'Currencies List App')

    def test_load_index_page(self):
        result = self.controller.load_index_page()
        self.assertIn('Currencies List App', result)
        self.assertIn('Currencies List App', result)
        self.assertIn('Currencies List App', result)

        # Test route users
        result = self.controller.load_users_page()
        self.assertIn('Users', result)

    def test_load_currency_page(self):
        # return_value = ({'USD': 75.5}, '05.12.2025')
        result = self.controller.load_currencies_page('USD')
        self.assertIn('USD', result)

    def test_load_users_page(self):
        result = self.controller.load_users_page()
        self.assertIn("id".lower(), result.lower())
        self.assertIn("Phan Tuan Anh".lower(), result.lower())
        self.assertIn("Duong Nhan Hau".lower(), result.lower())
        self.assertIn("Truong Tuan Kiet".lower(), result.lower())
        self.assertIn("Tang Vu Hoang Nguyen".lower(), result.lower())
        self.assertIn("Nguyen Dinh Sinh Phuoc".lower(), result.lower())
        self.assertIn("Nguyen Xuan Canh".lower(), result.lower())

    def test_load_user_page_by_ID(self):
        result = self.controller.load_user_page_by_ID(1)
        self.assertIn('Phan Tuan Anh', result)

    def test_user_by_id_not_found(self):
        result = self.controller.load_user_page_by_ID(999)
        self.assertIn('User with id = 999 not found!'.lower(), result.lower())

    def test_load_all_currencies_page(self):
        result = self.controller.load_all_currencies_page()
        self.assertIn('Currencies List App', result)
        self.assertIn('Currency ID:', result)
        self.assertIn('Currency numcode:', result)
        self.assertIn('Currency charcode:', result)
        self.assertIn('Currency name:', result)
        self.assertIn('Currency value:', result)
        self.assertIn('Currency nominal:', result)

class TestGetCurrencies(unittest.TestCase):
    def test_get_currencies(self):
        self.assertIn('USD', str(get_currencies(["Usd"])))
        self.assertIn('Код валюты \'blabla\' не найден.', str(get_currencies(["blabla"])))
        self.assertRegex(get_currencies(["blabla"])[1], r"\d{2}.\d{2}.\d{4}")

if __name__ == '__main__':
    unittest.main()

# Запуск тестов
# unittest.main(argv=[''], verbosity=2, exit=False)