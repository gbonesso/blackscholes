import logging
from math import log, sqrt, exp
from scipy.stats import norm

from blackscholes import pricing


def call_implied_volatility(S0, K, T, r, C0, sigma_est, it=100):
    """
    Implied Volatility of European call option in BSM Model.
    :param S0:
    :param K:
    :param T:
    :param r:
    :param C0:
    :param sigma_est:
    :param it:
    :return:
    """

    sigma_step = 0.01  # 1%
    direction = 0  # undefined
    for i in range(it):
        _call_value = pricing.call_value(S0, K, T, r, sigma_est)

        if _call_value < C0:  # sigma_est < implied volatility
            if direction == -1:  # Changing direction of step
                sigma_step = sigma_step * 0.1  # Make smaller steps
            direction = 1  # up
            sigma_est += sigma_step
        else:
            if direction == 1:  # Changing direction of step
                sigma_step = sigma_step * 0.1  # Make smaller steps
            direction = -1  # down
            sigma_est -= sigma_step

        # print('Estimated Call Value: {} - Market Call Value: {} - Sigma Est: {} - Sigma Step: {}'.
        #      format(_call_value, C0, sigma_est, sigma_step))

        if round(_call_value, 3) == round(C0, 3):
            break

        if sigma_est < 0.01:
            # Implied volatility cannot be negative...
            sigma_est = 0
            break
    return sigma_est


def put_implied_volatility(spot_price, strike_price, time_to_maturity,
                           risk_free_rate, option_price, initial_sigma, it=100):
    """
    Implied Volatility of European put option in BSM Model.
    :param spot_price:
    :param strike_price:
    :param time_to_maturity:
    :param risk_free_rate:
    :param option_price:
    :param initial_sigma:
    :param it:
    :return:
    """
    sigma_step = 0.01  # 1%
    direction = 0  # undefined
    guessed_sigma = initial_sigma
    for i in range(it):
        option_value = pricing.put_value(spot_price, strike_price, time_to_maturity, risk_free_rate, guessed_sigma)

        if option_value < option_price:  # initial_sigma < implied volatility
            if direction == -1:  # Changing direction of step
                sigma_step = sigma_step * 0.1  # Make smaller steps
            direction = 1  # up
            guessed_sigma += sigma_step
        else:
            if direction == 1:  # Changing direction of step
                sigma_step = sigma_step * 0.1  # Make smaller steps
            direction = -1  # down
            guessed_sigma -= sigma_step

        logging.debug('Estimated Put Value: {} - Market Call Value: {} - Sigma Est: {} - Sigma Step: {}'.
                      format(option_value, option_price, guessed_sigma, sigma_step))

        if round(option_value, 3) == round(option_price, 3):
            break

        if guessed_sigma < 0.01:
            # Implied volatility cannot be negative...
            guessed_sigma = 0
            break
    return guessed_sigma


def d1(spot_price, strike_price, time_to_maturity, risk_free_rate, sigma):
    try:
        numerator = log(spot_price / strike_price) + (risk_free_rate + sigma ** 2 / 2.) * time_to_maturity
        result = numerator / (sigma * sqrt(time_to_maturity))
    except ZeroDivisionError:
        logging.debug('d1 numerator: {}'.format(numerator))
        if numerator >= 0:
            result = float('inf')
        else:
            result = float('-inf')

    return result


def d2(spot_price, strike_price, time_to_maturity, risk_free_rate, sigma):
    return d1(spot_price, strike_price, time_to_maturity, risk_free_rate, sigma) - sigma * sqrt(time_to_maturity)


def call_delta(spot_price, strike_price, time_to_maturity, risk_free_rate, sigma):
    """
    TODO: Tratar o caso onde a volatilidade é zero (delta = 1?)
    :param spot_price:
    :param strike_price:
    :param time_to_maturity:
    :param risk_free_rate:
    :param sigma:
    :return:
    """
    return norm.cdf(d1(spot_price, strike_price, time_to_maturity, risk_free_rate, sigma))


def put_delta(spot_price, strike_price, time_to_maturity, risk_free_rate, sigma):
    return norm.cdf(d1(spot_price, strike_price, time_to_maturity, risk_free_rate, sigma)) - 1


def call_gamma(S, K, T, r, sigma):
    return norm.pdf(d1(S, K, T, r, sigma)) / (S * sigma * sqrt(T))


def call_vega(S, K, T, r, sigma):
    """
    I dropped the 0.01 normalization from the result.
    :param S:
    :param K:
    :param T:
    :param r:
    :param sigma:
    :return:
    """
    return (S * norm.pdf(d1(S, K, T, r, sigma)) * sqrt(T))


# Another formula: https://www.macroption.com/black-scholes-formula/#theta
def call_theta(S, K, T, r, sigma):
    """

    :param S: Asset spot price
    :param K: Strike price
    :param T: Time to maturity (in years)
    :param r: Risk free rate
    :param sigma: Volatility
    :return: Theta in years. Can be normalized in days dividing by 365.
    """
    return (-(S * norm.pdf(d1(S, K, T, r, sigma)) * sigma) / (2 * sqrt(T)) - r * K * exp(-r * T) * norm.cdf(
        d2(S, K, T, r, sigma)))


# wallstreet implementation (by differential)
def call_theta_dif(S, K, T, r, sigma):
    THETA_DIFFERENTIAL = 1.e-5
    h = THETA_DIFFERENTIAL

    p1 = pricing.call_value(S, K, T + h, r, sigma)
    p2 = pricing.call_value(S, K, T - h, r, sigma)

    # p1 = self.BS(self.S, self.K, self.T + h, self.impvol, self.r, self.q)
    # p2 = self.BS(self.S, self.K, self.T - h, self.impvol, self.r, self.q)
    return (p1 - p2) / (2 * h * 365)


def call_rho(S, K, T, r, sigma):
    return 0.01 * (K * T * exp(-r * T) * norm.cdf(d2(S, K, T, r, sigma)))
