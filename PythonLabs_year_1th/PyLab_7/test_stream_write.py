import unittest
import io
from logger import logger
import requests
from get_currencies import get_currencies

# Тесты
class TestStreamWrite(unittest.TestCase):

  def setUp(self):
    self.stream = io.StringIO()

    @logger(handle=self.stream)
    def success_wrapped():
      return get_currencies(['USD'], url="https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.2025")
    
    @logger(handle=self.stream)
    def error_wrapped():
      return get_currencies(['USD'], url="https://invalid")
    
    self.success_wrapped = success_wrapped
    self.error_wrapped = error_wrapped

  def test_logging_success(self):
    self.success_wrapped()

    logs = self.stream.getvalue()
    self.assertIn("INFO", logs)

  def test_logging_error(self):
    # with self.assertRaises(ConnectionError):
    with self.assertRaises(requests.exceptions.RequestException):
      self.error_wrapped()

    logs = self.stream.getvalue()
    # self.assertIn("ConnectionError", logs)
    self.assertIn("ERROR", logs)

# Запуск тестов
unittest.main(argv=[''], verbosity=2, exit=False)
