import sys
import unittest
import logging

from blackscholes import greeks

logger = logging.getLogger()
logger.level = logging.DEBUG


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

    def test_call_delta_sigma_zero_otm(self):
        """
        spot_price < strike_price
        """
        self.assertEqual(round(greeks.call_delta(5, 10, 1.0, 0.05, 0), 3), 0.000)

    def test_call_delta_sigma_zero_itm(self):
        """
        spot_price > strike_price
        """
        self.assertEqual(round(greeks.call_delta(15, 10, 1.0, 0.05, 0), 3), 1.000)

    def test_put_delta(self):
        """
        Exemplo 19.1 pag 438 Hull
        S0=49, K=50, r=0.05, sigma=0.2 e T=0.3846
        """
        self.assertEqual(round(greeks.put_delta(49, 50, 0.3846, 0.05, 0.2), 3), -0.478)

    def test_put_delta_sigma_zero_itm(self):
        """
        spot_price < strike_price
        """
        self.assertEqual(round(greeks.put_delta(5, 10, 1.0, 0.05, 0), 3), -1.000)

    def test_put_delta_sigma_zero_otm(self):
        """
        spot_price > strike_price
        """
        self.assertEqual(round(greeks.put_delta(15, 10, 1.0, 0.05, 0), 3), -0.000)

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
        self.assertEqual(round(greeks.call_implied_volatility(21, 20, 0.25, 0.1, 1.875, 0.2), 3), 0.234)

    def test_put_implied_volatility(self):
        """
        S0=26.33, K=26.46, T=7/365, r=0.025, C0=0.62, sigma (initial estimate)=0.2
        Implied Volatility=38.3%
        """
        self.assertEqual(round(greeks.put_implied_volatility(26.33, 26.46, 7/365, 0.025, 0.62, 0.2), 3), 0.383)

    def test_put_implied_volatility_strating_high(self):
        """
        S0=26.33, K=26.46, T=7/365, r=0.025, C0=0.62, sigma (initial estimate)=0.5
        Implied Volatility=38.3%
        """
        self.assertEqual(round(greeks.put_implied_volatility(26.33, 26.46, 7/365, 0.025, 0.62, 0.5), 3), 0.384)

    def test_call_implied_volatility_starting_high(self):
        """
        Section 15.11 page 365 Hull
        S0=21, K=20, r=0.1, sigma (initial estimate)=0.5, C0=1.875 e T=0.25
        The difference from the prior test is the initial estimated volatility higher than the implied volatility
        """
        self.assertEqual(round(greeks.call_implied_volatility(21, 20, 0.25, 0.1, 1.875, 0.5), 3), 0.234)

    def test_call_implied_volatility_floating_error(self):
        """
        Implied volatility cannot be negative. In this case the market price were too low...
        """
        self.assertEqual(round(greeks.call_implied_volatility(16.0578, 15, 1.7863013698630137, 0.025, 1.65, 0.2), 3), 0.000)

    def test_call_implied_volatility_floating_error_2(self):
        """
        Implied volatility cannot be negative. In this case the market price were too low...
        """
        self.assertEqual(round(greeks.call_implied_volatility(16.1485, 15, 1.7863013698630137, 0.025, 1.63, 0.2), 3), 0.000)


if __name__ == '__main__':
    """stream_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stream_handler)
    logging.basicConfig(filename='./log/TestGreeks.log', level=logging.DEBUG)
    logging.debug('\n\nIniciando TestGreeks\n\n')"""

    unittest.main()
