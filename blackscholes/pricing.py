import logging

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
    if sigma > 0:
        d1 = greeks.d1(spot, strike, time_to_maturity, risk_free_rate, sigma)
        d2 = greeks.d2(spot, strike, time_to_maturity, risk_free_rate, sigma)
        norm_cdf_d1 = stats.norm.cdf(d1, 0.0, 1.0)
        norm_cdf_d2 = stats.norm.cdf(d2, 0.0, 1.0)
    else:
        norm_cdf_d1 = 1.0
        norm_cdf_d2 = 1.0
    value = spot * norm_cdf_d1 - strike * exp(-risk_free_rate * time_to_maturity) * norm_cdf_d2
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
    _call_value = call_value(spot, strike, time_to_maturity, risk_free_rate, sigma)
    _put_value = _call_value - spot + exp(-risk_free_rate * time_to_maturity) * strike

    logging.debug('Call Value: {} - Put Value: {}'.
                  format(_call_value, _put_value))

    return _put_value
