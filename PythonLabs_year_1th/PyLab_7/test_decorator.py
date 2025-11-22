import unittest
import sys
from logger import logger
from get_currencies import get_currencies
from unittest.mock import patch
from io import StringIO

class test_decorator(unittest.TestCase):
    def setUp(self):
        self.get_logs()
        self.get_err_logs()

    def make_wrapper_func(self, handle):
        @logger(handle=handle)
        def wrapper(currency_code: list, url: str):
            get_currencies(currency_code, url)
        return wrapper
    
    @patch('sys.stdout', new_callable=StringIO)
    def get_logs(self, mock_stdout):
        currency_list = ["AUD", "USD", "EUR"]
        currency_url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.2025"
        wrapper = self.make_wrapper_func(mock_stdout)
        wrapper(currency_list, currency_url)
        logs = mock_stdout.getvalue()
        self.logs = logs
    
    @patch('sys.stdout', new_callable=StringIO)
    def get_err_logs(self, mock_err_stdout):
        currency_list = ["AUD", "USD", "EUR"]
        err_currency_url = "https://www.cbr.ru/scripts/XML_daily.asp?date_req=09.10.3000"
        wrapper = self.make_wrapper_func(mock_err_stdout)
        try:
            wrapper(currency_list, err_currency_url)
        except Exception as e:
            pass
        err_logs = mock_err_stdout.getvalue()
        self.err_logs = err_logs

    def test_args_message(self):
        self.assertIn("Function", self.logs)
        self.assertIn("starting with args", self.logs)

    def test_result_message(self):
        self.assertIn("Function", self.logs)
        self.assertIn("finished successfully with result", self.logs)

    def test_err_message(self):
        self.assertIn("Exception", self.err_logs)
        self.assertIn("occurred in function", self.err_logs)

unittest.main(argv=[''], verbosity=2, exit=False)