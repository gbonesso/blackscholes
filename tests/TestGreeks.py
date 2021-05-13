import unittest
from blackscholes import greeks


# https://docs.python.org/3/library/unittest.html
class TestGreeks(unittest.TestCase):

    def test_d1(self):
        """Exemplo 15.6 pag 362 Hull"""
        self.assertEqual(round(greeks.d1(42, 40, 0.5, 0.1, 0.2), 4), 0.7693)

    def test_d2(self):
        """Exemplo 15.6 pag 362 Hull"""
        self.assertEqual(round(greeks.d2(42, 40, 0.5, 0.1, 0.2), 4), 0.6278)

    def test_call_delta(self):
        """
        Exemplo 19.1 pag 438 Hull
        S0=49, K=50, r=0.05, sigma=0.2 e T=0.3846
        """
        self.assertEqual(round(greeks.call_delta(49, 50, 0.3846, 0.05, 0.2), 3), 0.522)

    def test_call_gamma(self):
        """
        Exemplo 19.4 pag 447 Hull
        S0=49, K=50, r=0.05, sigma=0.2 e T=0.3846
        """
        self.assertEqual(round(greeks.call_gamma(49, 50, 0.3846, 0.05, 0.2), 3), 0.066)

    def test_call_vega(self):
        """
        Exemplo 19.6 pag 450 Hull
        S0=49, K=50, r=0.05, sigma=0.2 e T=0.3846
        """
        self.assertEqual(round(greeks.call_vega(49, 50, 0.3846, 0.05, 0.2), 1), 12.1)

    def test_call_theta(self):
        """
        Exemplo 19.6 pag 450 Hull
        S0=49, K=50, r=0.05, sigma=0.2 e T=0.3846
        """
        self.assertEqual(round(greeks.call_theta(49, 50, 0.3846, 0.05, 0.2), 2), -4.31)

    def test_call_rho(self):
        """
        Exemplo 19.7 pag 452 Hull
        S0=49, K=50, r=0.05, sigma=0.2 e T=0.3846
        """
        self.assertEqual(round(greeks.call_rho(49, 50, 0.3846, 0.05, 0.2), 4), 0.0891)

    def test_call_implied_volatility(self):
        """
        Section 15.11 page 365 Hull
        S0=21, K=20, r=0.1, sigma (initial estimate)=0.2, C0=1.875 e T=0.25
        """
        self.assertEqual(round(greeks.call_implied_volatility(21, 20, 0.25, 0.1, 1.875, 0.2), 3), 0.235)

    def test_call_implied_volatility_floating_error(self):
        self.assertEqual(round(greeks.call_implied_volatility(16.0578, 15, 1.7863013698630137, 0.025, 1.65, 0.2), 3), 0.292)


if __name__ == '__main__':
    unittest.main()
