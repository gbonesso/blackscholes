from math import log, sqrt, exp
from scipy.stats import norm

from blackscholes import pricing


"""def dN(x):
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
"""

# Implied volatility function


def call_implied_volatility_old(S0, K, T, r, C0, sigma_est, it=100):
    """
    Implied Volatility of European call option in BSM Model.
    TODO: Why in some cases the call_value is negative?
    TODO: Understand the case where call_vega is zero
    :param S0:
    :param K:
    :param T:
    :param r:
    :param C0:
    :param sigma_est:
    :param it:
    :return:
    """
    for i in range(it):
        _call_value = pricing.call_value(S0, K, T, r, sigma_est)
        _call_vega = call_vega(S0, K, T, r, sigma_est) # * 0.01
        #if _call_vega < 0.001:
        #    _call_vega = 0.01

        if round(_call_value, 3) == round(C0, 3):
            break

        sigma_step = (_call_value - C0) / _call_vega
        # sigma_step = sigma_step * 0.1
        #if (sigma_step > 0) and (sigma_step < sigma_est):
        sigma_est -= sigma_step
        #else:
        #    sigma_est += sigma_step

        #if sigma_est < 0:
        #    sigma_est = -sigma_est
        print('Estimated Call Value: {} - Market Call Value: {} - Vega: {} - Sigma Est: {}'.
              format(_call_value, C0, _call_vega, sigma_est))
    return sigma_est


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

def d1(S, K, T, r, sigma):
    return(log(S/K)+(r+sigma**2/2.)*T)/(sigma*sqrt(T))


def d2(S,K,T,r,sigma):
    return d1(S,K,T,r,sigma)-sigma*sqrt(T)


def call_delta(S,K,T,r,sigma):
    return norm.cdf(d1(S,K,T,r,sigma))


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