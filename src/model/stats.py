import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
import pandas as pd


def fit_rolling_ols(y: pd.Series, X: pd.Series, window: int = 50) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Fit a rolling OLS regression to the given data. This computes the OLS fit of y = alpha + beta * X + residuals over
    the last `window` observations. The regression coefficients alpha and beta are returned as time series as well as
    the residuals of the regression.
    :param y:       Time series of one asset.
    :param X:       Time serios of another asset.
    :param window:  Window size for the rolling regression.
    :return:        Regression coefficients alpha, beta and the residuals as a time series.
    """
    rolling_ols = RollingOLS(y, sm.add_constant(X), window=window).fit()
    alpha = rolling_ols.params['const']
    beta = rolling_ols.params[X.name]
    residuals = y - (alpha + beta * X)
    return alpha, beta, residuals


def z_score(residuals: pd.Series, window: int = 50) -> pd.Series:
    """
    Compute the z-score of the residuals.
    :param residuals: Time series of residuals from a regression.
    :param window:    Window size for the rolling z-score calculation.
    :return:          Z-score of the residuals.
    """
    mu = residuals.rolling(window=window).mean()
    sigma = residuals.rolling(window=window).std()
    return (residuals - mu) / sigma
