import unittest
from parsers import parse_sber_ats
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class StartTestCase(unittest.TestCase):
    """
    Base class for all tests
    """
    def setUp(self) -> None:
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)  # /usr/local/bin

    def tearDown(self) -> None:
        self.addCleanup(self.browser.close)


class ConnectioCheck(StartTestCase):
    def testUrl(self):
        self.browser.get('https://sberbank-ast.ru')
        self.assertIn('https://sberbank-ast.ru', self.browser.current_url)
