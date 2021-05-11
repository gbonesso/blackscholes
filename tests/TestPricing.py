import unittest
from blackscholes import pricing


# https://docs.python.org/3/library/unittest.html
class TestPricing(unittest.TestCase):

    def test_call_value(self):
        """
        Exemplo 15.6 pag 362 Hull
        S0=42, K=40, r=0.1, sigma=0.2 e T=0.5
        """
        self.assertEqual(round(pricing.call_value(42, 40, 0.5, 0.1, 0.2), 2), 4.76)

    def test_put_value(self):
        """
        Exemplo 15.6 pag 362 Hull
        S0=42, K=40, r=0.1, sigma=0.2 e T=0.5
        """
        self.assertEqual(round(pricing.put_value(42, 40, 0.5, 0.1, 0.2), 2), 0.81)


if __name__ == '__main__':
    unittest.main()
