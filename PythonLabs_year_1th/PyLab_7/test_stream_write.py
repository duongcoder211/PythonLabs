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
    def wrapped():
      return get_currencies(['USD'], url="https://invalid")
    
    self.wrapped = wrapped

  def test_logging_error(self):
    # with self.assertRaises(ConnectionError):
    with self.assertRaises(requests.exceptions.RequestException):
      self.wrapped()

    logs = self.stream.getvalue()
    # self.assertIn("ConnectionError", logs)
    self.assertIn("ERROR", logs)

# Запуск тестов
unittest.main(argv=[''], verbosity=2, exit=False)