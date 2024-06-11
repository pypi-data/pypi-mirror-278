import numpy as np
from scipy.stats import norm, linregress

# ======== STATS ========


def comp(returns):
    """Calculates total compounded returns"""
    return returns.add(1).prod() - 1


def geometric_mean(returns):
    """Shorthand for expected_return()"""
    return np.product(1 + returns) ** (1 / len(returns)) - 1


def win_rate(returns):
    """Calculates the win ratio for a period"""
    def _win_rate(series):
        try:
            return len(series[series > 0]) / len(series[series != 0])
        except Exception:
            return 0.

    return _win_rate(returns)


def avg_win(returns):
    """
    Calculates the average winning
    return/trade return for a period
    """
    return returns[returns > 0].dropna().mean()


def avg_loss(returns):
    """
    Calculates the average low if
    return/trade return for a period
    """
    return returns[returns < 0].dropna().mean()


def autocorr_penalty(returns):
    """Metric to account for auto correlation"""

    # returns.to_csv('/Users/ran/Desktop/test.csv')
    num = len(returns)
    coef = np.abs(np.corrcoef(returns[:-1], returns[1:])[0, 1])
    corr = [((num - x)/num) * coef ** x for x in range(1, num)]
    return np.sqrt(1 + 2 * np.sum(corr))


# ======= METRICS =======

def sharpe(returns, rf=0., periods=252, annualize=True, smart=False):
    """
    Calculates the sharpe ratio of access returns
    If rf is non-zero, you must specify periods.
    In this case, rf is assumed to be expressed in yearly (annualized) terms
    Args:
        * returns (Series, DataFrame): Input return series
        * rf (float): Risk-free rate expressed as a yearly (annualized) return
        * periods (int): Freq. of returns (252/365 for daily, 12 for monthly)
        * annualize: return annualize sharpe?
        * smart: return smart sharpe ratio
    """
    if rf != 0 and periods is None:
        raise Exception('Must provide periods if rf != 0')

    divisor = returns.std(ddof=1)
    if smart:
        # penalize sharpe with auto correlation
        divisor = divisor * autocorr_penalty(returns)
    res = returns.mean() / divisor

    if annualize:
        return res * np.sqrt(1 if periods is None else periods)

    return res


def sortino(returns, rf=0, periods=252, annualize=True, smart=False):
    """
    Calculates the sortino ratio of access returns
    If rf is non-zero, you must specify periods.
    In this case, rf is assumed to be expressed in yearly (annualized) terms
    Calculation is based on this paper by Red Rock Capital
    http://www.redrockcapital.com/Sortino__A__Sharper__Ratio_Red_Rock_Capital.pdf
    """
    downside = np.sqrt((returns[returns < 0] ** 2).sum() / len(returns))

    if smart:
        # penalize sortino with auto correlation
        downside = downside * autocorr_penalty(returns)

    res = returns.mean() / downside

    if annualize:
        return res * np.sqrt(
            1 if periods is None else periods)

    return res


def adjusted_sortino(returns, rf=0, periods=252, annualize=True, smart=False):
    """
    Jack Schwager's version of the Sortino ratio allows for
    direct comparisons to the Sharpe. See here for more info:
    https://archive.is/wip/2rwFW
    """
    data = sortino(returns, rf, periods=periods, annualize=annualize, smart=smart)
    return data / np.sqrt(2)


def probabilistic_ratio(metric, returns, rf=0., annualize=False):
    skew_no = skew(returns)
    kurtosis_no = kurtosis(returns)

    n = len(returns)

    sigma_sr = np.sqrt(
        (1 + (0.5 * metric ** 2) - (skew_no * metric) + (((kurtosis_no - 3) / 4) * metric ** 2)) / (n - 1)
    )

    ratio = (metric - rf) / sigma_sr
    psr = norm.cdf(ratio)

    if annualize:
        return psr * (252 ** 0.5)
    return psr


def cagr(returns, rf=0., compounded=True):
    """
    Calculates the communicative annualized growth return
    (CAGR%) of access returns
    If rf is non-zero, you must specify periods.
    In this case, rf is assumed to be expressed in yearly (annualized) terms
    """
    total = returns
    if compounded:
        total = comp(total)
    else:
        total = np.sum(total)

    years = (returns.index[-1] - returns.index[0]).days / 365.

    return abs(total + 1.0) ** (1.0 / years) - 1


def skew(returns):
    """
    Calculates returns' skewness
    (the degree of asymmetry of a distribution around its mean)
    """
    return returns.skew()


def kurtosis(returns):
    """
    Calculates returns' kurtosis
    (the degree to which a distribution peak compared to a normal distribution)
    """
    return returns.kurtosis()


def calmar(returns):
    """Calculates the calmar ratio (CAGR% / MaxDD%)"""
    cagr_ratio = cagr(returns)
    max_dd = max_drawdown(returns)
    return cagr_ratio / abs(max_dd)


def risk_of_ruin(returns):
    """
    RoR
    Calculates the risk of ruin
    (the likelihood of losing all one's investment capital)
    """
    wins = win_rate(returns)
    return ((1 - wins) / (1 + wins)) ** len(returns)


def value_at_risk(returns, sigma=1, confidence=0.95):
    """
    Var
    Calculates the daily value-at-risk
    (variance-covariance calculation with confidence n)
    """
    mu = returns.mean()
    sigma *= returns.std()

    if confidence > 1:
        confidence = confidence/100

    return norm.ppf(1-confidence, mu, sigma)


def conditional_value_at_risk(returns, sigma=1, confidence=0.95):
    """
    CVar, expected_shortfall
    Calculates the conditional daily value-at-risk (aka expected shortfall)
    quantifies the amount of tail risk an investment
    """
    var = value_at_risk(returns, sigma, confidence)
    c_var = returns[returns < var].values.mean()
    return c_var if ~np.isnan(c_var) else var


def tail_ratio(returns, cutoff=0.95):
    """
    Measures the ratio between the right
    (95%) and left tail (5%).
    """
    return abs(returns.quantile(cutoff) / returns.quantile(1-cutoff))


def payoff_ratio(returns):
    """Measures the payoff ratio (average win/average loss)"""
    return avg_win(returns) / abs(avg_loss(returns))


def profit_ratio(returns):
    """Measures the profit ratio (win ratio / loss ratio)"""
    wins = returns[returns >= 0]
    loss = returns[returns < 0]

    win_ratio = abs(wins.mean() / wins.count())
    loss_ratio = abs(loss.mean() / loss.count())
    return np.divide(win_ratio, loss_ratio)


def profit_factor(returns):
    """Measures the profit ratio (wins/loss)"""
    return abs(returns[returns >= 0].sum() / returns[returns < 0].sum())


def recovery_factor(returns):
    """Measures how fast the strategy recovers from drawdowns"""
    total_returns = comp(returns)
    max_dd = max_drawdown(returns)
    return total_returns / abs(max_dd)


def max_drawdown(prices):
    """Calculates the maximum drawdown"""
    return (prices / prices.expanding(min_periods=0).max()).min() - 1


def to_drawdown_series(returns):
    """Convert returns series to drawdown series"""
    dd = prices / np.maximum.accumulate(prices) - 1.
    return dd.replace([np.inf, -np.inf, -0], 0)


def kelly_criterion(returns):
    """
    Calculates the recommended maximum amount of capital that
    should be allocated to the given strategy, based on the
    Kelly Criterion (http://en.wikipedia.org/wiki/Kelly_criterion)
    """
    win_loss_ratio = payoff_ratio(returns)
    win_prob = win_rate(returns)
    lose_prob = 1 - win_prob

    return ((win_loss_ratio * win_prob) - lose_prob) / win_loss_ratio
