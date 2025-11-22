import unittest
import requests
import requests.exceptions
import xml.parsers
from get_currencies import get_currencies

MAX_R_VALUE = 1000

# Тесты
class TestGetCurrencies(unittest.TestCase):

  def test_currency_aud(self):
    """
      Проверяет наличие ключа в словаре и значения этого ключа
    """
    currency_list = ['AUD', 'USD', 'EUR', 'GBP', 'NNZ']
    currency_data = get_currencies(currency_list)

    self.assertIn(currency_list[0], currency_data)
    self.assertIsInstance(currency_data['AUD'], float)
    self.assertGreaterEqual(currency_data['AUD'], 0)
    self.assertLessEqual(currency_data['AUD'], MAX_R_VALUE)

  def test_nonexist_code(self):
    self.assertIn("Код валюты", get_currencies(['XYZ'])['XYZ'])
    self.assertIn("XYZ", get_currencies(['XYZ'])['XYZ'])
    self.assertIn("не найден", get_currencies(['XYZ'])['XYZ'])

  def test_get_currency_error(self):
    re_error_phrase_regex = "Ошибка при запросе к API"
    ce_error_phrase_regex = "API недоступен"
    ke_error_phrase_regex = "Нет ключа “Valute”"
    ee_error_phrase_regex = "Некорректный XML"
    te_error_phrase_regex = "Курс валюты имеет неверный тип"
    currency_list = ['AUD']


    with self.assertRaises(requests.exceptions.RequestException) as re:
      get_currencies(currency_list, url="https://")
      self.assertRegex(re_error_phrase_regex, re.exception)
    
    # ConnectionError is a RequestException subclass 
    # with self.assertRaises(requests.exceptions.ConnectionError) as ce:
    #   get_currencies(currency_list, url="https://blablabalabalabala.com")
    #   self.assertRegex(ce_error_phrase_regex, str(ce.exception))

    with self.assertRaises(xml.parsers.expat.ExpatError) as ee:
      get_currencies(currency_list, url="https://www.cbr-xml-daily.ru/daily_json.js")
      self.assertRegex(ee_error_phrase_regex, ee.exception)
    
    with self.assertRaises(KeyError) as ke:
      get_currencies(currency_list, url="https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.2030")
      self.assertRegex(ke_error_phrase_regex, ke.exception)
    
    with self.assertRaises(TypeError) as te:
      get_currencies(currency_codes=123, url="https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.2025")
      self.assertRegex(te_error_phrase_regex, te.exception)

    # with self.assertRaisesRegex(requests.exceptions.RequestException, re_error_phrase_regex):
    #   get_currencies(currency_list, url="https://")

    # # with self.assertRaisesRegex(ConnectionError, ce_error_phrase_regex):
    # #   get_currencies(currency_list, url="https://www.cbr.ru/scripts/XML_daily.asp?date_req=hello")

    # with self.assertRaisesRegex(xml.parsers.expat.ExpatError, ee_error_phrase_regex):
    #   get_currencies(currency_list, url="https://www.cbr-xml-daily.ru/daily_json.js")

    # with self.assertRaisesRegex(KeyError, ke_error_phrase_regex):
    #   get_currencies(currency_list, url="https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.2030")

    # with self.assertRaisesRegex(TypeError, te_error_phrase_regex):
    #   get_currencies(currency_codes=123, url="https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.2025")
      

  #   # Найти каким образом проверить содержание фразы error_phase_regex в
  #   # потоке вывода

  #   # Дополнить тест, который должен проверять что в потоке, куда пишет функция
  #   # get_currencies содержится error_phrase_regex /
  #   # для использования assertStartsWith или assertRegex

# Запуск тестов
unittest.main(argv=[''], verbosity=2, exit=False)