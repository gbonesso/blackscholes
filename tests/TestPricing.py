import logging
import unittest
from blackscholes import pricing

logger = logging.getLogger()
logger.level = logging.DEBUG


# https://docs.python.org/3/library/unittest.html
class TestPricing(unittest.TestCase):

    def test_call_value(self):
        """
        Exemplo 15.6 pag 362 Hull
        S0=42, K=40, r=0.1, sigma=0.2 e T=0.5
        """
        self.assertEqual(round(pricing.call_value(42, 40, 0.5, 0.1, 0.2), 2), 4.76)

    def test_call_value_sigma_zero(self):
        """
        """
        self.assertEqual(round(pricing.call_value(11, 10, 1.0, 0.1, 0.0), 2), 1.95)

    def test_put_value(self):
        """
        Exemplo 15.6 pag 362 Hull
        S0=42, K=40, r=0.1, sigma=0.2 e T=0.5
        """
        self.assertEqual(round(pricing.put_value(42, 40, 0.5, 0.1, 0.2), 2), 0.81)

    def test_put_value_sigma_zero(self):
        """
        """
        self.assertEqual(round(pricing.put_value(11, 10, 1.0, 0.1, 0.0), 2), 1.95)

if __name__ == '__main__':
    unittest.main()
