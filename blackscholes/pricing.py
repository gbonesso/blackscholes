from scipy import stats
from math import exp
from blackscholes import greeks


def call_value(spot, strike, time_to_maturity, risk_free_rate, sigma):
    """

    :param spot:
    :param strike:
    :param time_to_maturity:
    :param risk_free_rate:
    :param sigma:
    :return:
    """
    d1 = greeks.d1(spot, strike, time_to_maturity, risk_free_rate, sigma)
    d2 = greeks.d2(spot, strike, time_to_maturity, risk_free_rate, sigma)
    value = (spot * stats.norm.cdf(d1, 0.0, 1.0)
             - strike * exp(-risk_free_rate * time_to_maturity) * stats.norm.cdf(d2, 0.0, 1.0))
    return value


def put_value(spot, strike, time_to_maturity, risk_free_rate, sigma):
    """

    :param spot:
    :param strike:
    :param time_to_maturity:
    :param risk_free_rate:
    :param sigma:
    :return:
    """
    value = call_value(spot, strike, time_to_maturity, risk_free_rate, sigma) \
            - spot + exp(-risk_free_rate * time_to_maturity) * strike
    return value
