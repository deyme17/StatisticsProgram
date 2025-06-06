from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats
import pandas as pd

class ExponentialDistribution(StatisticalDistribution):
    """Exponential distribution."""

    def __init__(self, lam=None):
        """
        :param lam: rate parameter (λ)
        """
        super().__init__()
        self.params = (lam,)
        self.color = 'yellow'
        self.name = 'Exponential'

    @property
    def distribution_params(self) -> dict[str, float | None]:
        """
        :return: {"lambda": λ}
        """
        return {"lambda": self.params[0] if self.params else None}

    def fit(self, data: pd.Series) -> tuple:
        """
        Fit exponential distribution to the given data.

        :param data: input data series
        :return: (lambda,)
        """
        min_val = np.nanmin(data)
        if min_val <= 0:
            data = data - min_val + 0.01

        mean = np.nanmean(data)
        if mean == 0:
            mean = 0.01
        self.params = (1 / mean,)
        return self.params

    def get_mean(self) -> float | None:
        """
        Return the theoretical mean of the fitted distribution.

        :return: mean value or None
        """
        if not self.params or self.params[0] == 0:
            return None
        lam = self.params[0]
        return 1 / lam

    def get_pdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        """
        Compute the PDF of the exponential distribution.

        :param x: array of evaluation points
        :param params: (lambda,)
        :return: array of PDF values
        """
        return stats.expon.pdf(x, loc=0, scale=1 / params[0] if params[0] > 0 else 1)

    def get_distribution_object(self, params: tuple):
        """
        Return a frozen scipy.stats.expon object with given parameters.

        :param params: (lambda,)
        :return: scipy.stats.rv_frozen object
        """
        return stats.expon(scale=1 / params[0]) if params[0] > 0 else stats.expon()

    def _get_plot_range(self, data: pd.Series) -> tuple[float, float]:
        """
        Define the plotting range for exponential distribution.

        :param data: input data series
        :return: (min x, max x)
        """
        min_val = np.nanmin(data)
        x_min = max(0, min_val * 0.8) if min_val > 0 else 0
        x_max = np.nanmax(data) * 1.2
        return x_min, x_max

    def get_cdf_variance(self, x_vals: np.ndarray, params: tuple, n: int) -> np.ndarray:
        """
        Compute the variance of the CDF estimate at given points.

        :param x_vals: array of evaluation points
        :param params: (lambda,)
        :param n: sample size
        :return: array of variances
        """
        lam = max(1e-10, params[0])
        # the limitation for safety
        expo = np.clip(2 * lam * x_vals, 0, 700)
        variance = (x_vals ** 2) * np.exp(-expo) * (lam ** 2) / n
        return np.nan_to_num(variance, nan=0.0, posinf=0.0, neginf=0.0)

    def get_inverse_cdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        """
        Compute the inverse CDF (quantile function) of the exponential distribution.

        :param x: array of probabilities in [0, 1]
        :param params: (lambda,)
        :return: array of quantiles
        """
        lam = params[0]
        return -np.log(1 - x) / lam