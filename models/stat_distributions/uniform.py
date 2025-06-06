from models.stat_distributions.stat_distribution import StatisticalDistribution
import numpy as np
from scipy import stats
import pandas as pd

class UniformDistribution(StatisticalDistribution):
    """Uniform distribution."""

    def __init__(self, a=None, b=None):
        """
        :param a: lower bound
        :param b: upper bound
        """
        super().__init__()
        self.color = 'purple'
        self.name = 'Uniform'
        self.params = (a, b) if a is not None and b is not None else None

    @property
    def distribution_params(self) -> dict[str, float | None]:
        """
        :return: {"a": lower bound, "b": upper bound}
        """
        return {
            "a": self.params[0] if self.params else None,
            "b": self.params[1] if self.params else None
        }

    def fit(self, data: pd.Series) -> tuple:
        """
        Fit uniform distribution to the given data.

        :param data: input data series
        :return: (a, b)
        """
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        if min_val == max_val:
            max_val = min_val + 0.01
        self.params = (min_val, max_val)
        return self.params

    def get_mean(self) -> float | None:
        """
        Return the theoretical mean of the fitted distribution.

        :return: mean value or None
        """
        if not self.params:
            return None
        a, b = self.params
        return (a + b) / 2

    def get_pdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        """
        Compute the PDF of the uniform distribution.

        :param x: array of evaluation points
        :param params: (a, b)
        :return: array of PDF values
        """
        return stats.uniform.pdf(x, loc=params[0], scale=params[1] - params[0])

    def get_distribution_object(self, params: tuple):
        """
        Return a frozen scipy.stats.uniform object with given parameters.

        :param params: (a, b)
        :return: scipy.stats.rv_frozen object
        """
        return stats.uniform(loc=params[0], scale=params[1] - params[0])

    def _get_plot_range(self, data: pd.Series) -> tuple[float, float]:
        """
        Define the plotting range for uniform distribution.

        :param data: input data series
        :return: (min x, max x)
        """
        params = self.fit(data)
        x_min = params[0] - 0.1 * (params[1] - params[0])
        x_max = params[1] + 0.1 * (params[1] - params[0])
        return x_min, x_max

    def get_cdf_variance(self, x_vals: np.ndarray, params: tuple, n: int) -> np.ndarray:
        """
        Compute the variance of the CDF estimate at given points.

        :param x_vals: array of evaluation points
        :param params: (a, b)
        :param n: sample size
        :return: array of variances
        """
        a, b = params

        var_a = (b - a)**2 / (12 * n)
        var_b = (b - a)**2 / (12 * n)
        cov_ab = 0

        denom = (b - a) ** 4
        term1 = ((x_vals - b) ** 2) * var_a / denom
        term2 = ((x_vals - a) ** 2) * var_b / denom
        term3 = -2 * (x_vals - a) * (x_vals - b) * cov_ab / denom

        variance = term1 + term2 + term3
        return variance

    def get_inverse_cdf(self, x: np.ndarray, params: tuple) -> np.ndarray:
        """
        Compute the inverse CDF (quantile function) of the uniform distribution.

        :param x: array of probabilities in [0, 1]
        :param params: (a, b)
        :return: array of quantiles
        """
        a = params[0]
        b = params[1] - params[0]
        return a + b * x
