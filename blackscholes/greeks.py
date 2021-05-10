## import certain packages
from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date
import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.integrate import quad


def dN(x):
    ''' Probability density function of standard normal random variable x. '''
    return exp(-0.5 * x ** 2) / sqrt(2 * pi)


def N(d):
    ''' Cumulative density function of standard normal random variable x. '''
    return quad(lambda x: dN(x), -20, d, limit=50)[0]


def d1f(St, K, t, T, r, sigma):
    ''' Black-Scholes-Merton d1 function.
        Parameters see e.g. BSM_call_value function. '''
    d1 = (log(St / K) + (r + 0.5 * sigma ** 2)
          * (T - t)) / (sigma * sqrt(T - t))
    return d1


def call_delta_old(St, K, t, T, r, sigma):
    ''' Black-Scholes-Merton DELTA of European call option.
    Parameters
    ==========
    St: float
    stock/index level at time t
    K: float
    strike price
    t: float
    valuation date
    T: float
    date of maturity/time-to-maturity if t = 0; T > t
    r: float
    constant, risk-less short rate
    sigma: float
    volatility
    Returns
    =======
    delta: float
    European call option DELTA
    '''
    d1 = d1f(St, K, t, T, r, sigma)
    delta = N(d1)
    return delta


def call_theta(St, K, t, T, r, sigma):
    ''' Black-Scholes-Merton THETA of European call option.

    Parameters
    ==========
    St : float
        stock/index level at time t
    K : float
        strike price
    t : float
        valuation date
    T : float
        date of maturity/time-to-maturity if t = 0; T > t
    r : float
        constant, risk-less short rate
    sigma : float
        volatility

    Returns
    =======
    theta : float
        European call option THETA
        The result is for one year. To get the daily theta the result should be divided by 365.
    '''
    d1 = d1f(St, K, t, T, r, sigma)
    d2 = d1 - sigma * sqrt(T - t)
    theta = -(St * dN(d1) * sigma / (2 * sqrt(T - t)) +
              r * K * exp(-r * (T - t)) * N(d2))
    return theta


def bsm_vega(S0, K, T, r, sigma):
    ''' Vega of European option in BSM Model.

    Parameters
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    T : float
        maturity date (in year fractions)
    r : float
        constant risk-free short rate
    sigma : float
        volatility factor in diffusion term

    Returns
    =======
    vega : float
        partial derivative of BSM formula with respect
        to sigma, i.e. Vega

    '''
    from math import log, sqrt
    from scipy import stats

    S0 = float(S0)
    d1 = (log(S0 / K) + (r + (0.5 * sigma ** 2) * T)) / (sigma * sqrt(T))
    # print(" - ", stats.norm.pdf(d1, 0.0, 1.0))
    vega = S0 * stats.norm.pdf(d1, 0.0, 1.0) * sqrt(T)
    return vega


# Implied volatility function


def bsm_call_imp_vol(S0, K, T, r, C0, sigma_est, it=100):
    ''' Implied Volatility of European call option in BSM Model.

    Parameters
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    T : float
        maturity date (in year fractions)
    r : float
        constant risk-free short rate
    sigma_est : float
        estimate of impl. volatility
    it : integer
        number of iterations

    Returns
    =======
    simga_est : float
        numerically estimated implied volatility
    '''
    for i in range(it):
        bsm_call_ = bsm_call_value(S0, K, T, r, sigma_est)
        bsm_vega_ = bsm_vega(S0, K, T, r, sigma_est)
        # print(bsm_call_, " - ", bsm_vega_)
        sigma_est -= (bsm_call_ - C0) / bsm_vega_
        # print("sigma_est: ", sigma_est)
    return sigma_est

# Other implementation...


def d1(S,K,T,r,sigma):
    return(log(S/K)+(r+sigma**2/2.)*T)/(sigma*sqrt(T))


def d2(S,K,T,r,sigma):
    return d1(S,K,T,r,sigma)-sigma*sqrt(T)


def call_delta(S,K,T,r,sigma):
    return norm.cdf(d1(S,K,T,r,sigma))


def call_gamma(S, K, T, r, sigma):
    return norm.pdf(d1(S, K, T, r, sigma)) / (S * sigma * sqrt(T))


def call_vega(S, K, T, r, sigma):
    return 0.01 * (S * norm.pdf(d1(S, K, T, r, sigma)) * sqrt(T))


# Another formula: https://www.macroption.com/black-scholes-formula/#theta
def call_theta(S, K, T, r, sigma):
    return 0.01 * (-(S * norm.pdf(d1(S, K, T, r, sigma)) * sigma) / (2 * sqrt(T)) - r * K * exp(-r * T) * norm.cdf(
        d2(S, K, T, r, sigma)))


# wallstreet implementation (by differential)
def call_theta_dif(S, K, T, r, sigma):
    THETA_DIFFERENTIAL = 1.e-5
    h = THETA_DIFFERENTIAL

    p1 = bsm_call_value(S, K, T + h, r, sigma)
    p2 = bsm_call_value(S, K, T - h, r, sigma)

    # p1 = self.BS(self.S, self.K, self.T + h, self.impvol, self.r, self.q)
    # p2 = self.BS(self.S, self.K, self.T - h, self.impvol, self.r, self.q)
    return (p1 - p2) / (2 * h * 365)


def call_rho(S, K, T, r, sigma):
    return 0.01 * (K * T * exp(-r * T) * norm.cdf(d2(S, K, T, r, sigma)))