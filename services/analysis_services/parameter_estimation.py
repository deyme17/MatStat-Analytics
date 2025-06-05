from models.stat_distributions import registered_distributions
from scipy.optimize import minimize
import numpy as np
import pandas as pd

limited_dists = ["Exponential", "Weibull"]

class ParameterEstimation:
    """
    Service for estimating distribution parameters using various methods.
    """
    def __init__(self):
        # Map estimation methods to their corresponding functions
        self._method_map = {
            "method_of_moments": lambda dist, data: dist.fit(data),
            "maximum_likelihood": self._estimate_maximum_likelihood
        }

    def estimate(self, dist_name: str, method: str, data: pd.Series) -> tuple | None:
        """
        Estimate parameters for the given distribution and method.

        :param dist_name: Name of the distribution (e.g., 'Normal', 'Weibull')
        :param method: Estimation method ('method_of_moments', 'maximum_likelihood')
        :param data: Input data series
        :return: Tuple of estimated parameters or None if failed
        """
        dist_class = registered_distributions.get(dist_name)
        if not dist_class:
            return None

        dist_instance = dist_class()

        try:
            method_func = self._method_map.get(method)
            if not method_func:
                return None
            return method_func(dist_instance, data)
        except:
            return None
        
    def _estimate_maximum_likelihood(self, dist_instance, data: pd.Series) -> tuple | None:
        """
        Estimate parameters using the Maximum Likelihood Estimation method.

        :param dist_instance: Instance of the distribution class
        :param data: Input data series
        :return: Tuple of estimated parameters or None if failed
        """
        def neg_log_likelihood(params, x, dist):
            try:
                pdf = dist.get_distribution_object(params).pdf(x)
                # Avoid log(0) by clipping
                pdf = np.clip(pdf, 1e-10, None)
                return -np.sum(np.log(pdf))
            except:
                return np.inf

        data = self.preprocess_limited_dists(dist_instance, data)
        x = data.dropna().values
        if len(x) == 0:
            return None

        # initial guess
        try:
            initial_guess = dist_instance.fit(data)
        except:
            return None

        # positive bounds to all parameters by default
        bounds = [(1e-10, None) for _ in initial_guess]

        try:
            result = minimize(
                neg_log_likelihood,
                initial_guess,
                args=(x, dist_instance),
                bounds=bounds,
                method='L-BFGS-B'
            )
            if result.success:
                return tuple(result.x)
            return None
        except:
            return None

    def preprocess_limited_dists(self, dist_instance, data: pd.Series) -> pd.Series:
        """
        Preprocess data for distributions that require positive values.

        :param dist_instance: Instance of the distribution class
        :param data: Input data series
        :return: Preprocessed data series
        """
        if dist_instance.name in limited_dists:
            min_val = np.nanmin(data)
            if min_val <= 0:
                data = data - min_val + 0.01
        return data