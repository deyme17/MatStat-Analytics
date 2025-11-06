import numpy as np
import pandas as pd
from typing import List, Optional, Dict
from scipy.stats import t
from models.stat_distributions.stat_distribution import StatisticalDistribution
from services.analysis_services.stat_tests import TestPerformer

class SimulationService:
    """
    Service for simulating samples from distributions and evaluating T-tests.
    """
    def __init__(self, test_performer: TestPerformer):
        """
        Initialize SimulationService with a StatisticsService instance.
        Args:
            test_performer: Service for performing statistical tests
        """
        self.test_performer: TestPerformer = test_performer

    def generate_sample(self, distribution: StatisticalDistribution, size: int, params: Dict) -> np.ndarray:
        """
        Generate a random sample from a distribution using the inverse CDF method.
        Args:
            distribution: instance of StatisticalDistribution
            size: number of values to generate
            params: distribution parameters
        Return:
            numpy array of sampled values
        """
        try:
            if not distribution.validate_params():
                return None
            u = np.random.uniform(0, 1, size)
            return distribution.get_inverse_cdf(u, params)
        except Exception as e:
            print(f"[SimulationService] Error in generate_sample: {e}")
            return None

    def run_experiment(self, distribution: StatisticalDistribution, sizes: List[int], n_repeat: int,
                       true_mean: float, alpha: float = 0.05) -> List[Dict]:
        """
        Run repeated T-tests on simulated samples of varying sizes.
        Args:
            distribution: instance of StatisticalDistribution
            sizes: list of sample sizes to test
            n_repeat: number of repetitions per sample size
            true_mean: theoretical mean to test against
            alpha: significance level for critical t-value
        Return:
            list of dictionaries with t-statistics summary and parameter estimates per sample size
        """
        results = []

        for size in sizes:
            t_stats = []
            param_estimates = []
            original_params = distribution.params

            for _ in range(n_repeat):
                sample = self.generate_sample(distribution, size, original_params)
                t_result = self.test_performer.perform_t_test(sample, true_mean=true_mean)
                t_stats.append(t_result['t_statistic'])
                dist_copy = type(distribution)()
                param_estimates.append(dist_copy.fit(pd.Series(sample)))

            distribution.params = original_params

            mean_t = np.mean(t_stats)
            std_t = np.std(t_stats, ddof=1)
            t_crit = t.ppf(1 - alpha / 2, df=size - 1)

            param_estimates = np.array(param_estimates) 
            params_mean = tuple(np.mean(param_estimates, axis=0)) 
            params_var = tuple(np.var(param_estimates, axis=0, ddof=1))

            results.append({
                'size': size,
                't_mean': mean_t,
                't_std': std_t,
                't_crit': t_crit,
                'params_mean': params_mean,
                'params_var': params_var
            })

        return results
    
    def generate_data(self, dist_cls: type[StatisticalDistribution], n_features: int,
                      params_list: list[tuple[float]], corr_coeffs: Optional[List[List[float]]], 
                      size: int) -> np.ndarray:
        """
        Generate multivariate correlated data from specified statistical distribution.
            Args:
                dist_cls: class of StatisticalDistribution (e.g. NormalDistribution)
                n_features: number of dimensions to generate
                params_list: list of parameter tuples for each feature
                corr_coeffs: correlation matrix or None
                size: sample size
        Returns:
            np.ndarray: Generated dataset with shape (size, n_features) with specified correlations
        """
        if len(params_list) != n_features:
            raise ValueError("Number of parameter sets must match n_features")
        
        dist = dist_cls()
        dist.params = params_list[0]

        if n_features == 1 or not corr_coeffs:
            sample = self.generate_sample(dist, size, dist.params)
            return sample.reshape(-1, 1) if sample is not None else None
        
        # validate correlation matrix
        self._validate_correlation_matrix(corr_coeffs, n_features)
        
        # generate independent samples for each feature
        independent_samples = np.zeros((size, n_features))
        for i in range(n_features):
            dist = dist_cls()
            dist.params = params_list[0]
            sample = self.generate_sample(dist, size, dist.params)
            if sample is None:
                return None
            independent_samples[:, i] = sample
        # apply correlation
        return self._apply_correlation(independent_samples, corr_coeffs)
    
    def _apply_correlation(self, data: np.ndarray, corr_matrix: List[List[float]]) -> np.ndarray:
        """
        Apply correlation structure to independent data using Cholesky decomposition.
        Args:
            data: Independent data with shape (n_samples, n_features)
            corr_matrix: Target correlation matrix
        Returns:
            Correlated data with approximately the target correlation structure
        """
        # standardize
        standardized = (data - np.mean(data, axis=0)) / np.std(data, axis=0, ddof=1)
        try:
            # calc Lapinskiy matrix
            L = np.linalg.cholesky(corr_matrix)
        except np.linalg.LinAlgError:
            raise ValueError("Correlation matrix is not positive definite")
        # apply transformation
        correlated = standardized @ L.T
        
        # original scale
        original_mean = np.mean(data, axis=0)
        original_std = np.std(data, axis=0, ddof=1)
        correlated = correlated * original_std + original_mean
        
        return correlated
    
    @staticmethod
    def _validate_correlation_matrix(corr_coeffs: List[List[float]], n_features: int) -> None:
        """
        Validate that correlation matrix is properly formatted and mathematically valid.
        Args:
            corr_coeffs: Correlation coefficients matrix
            n_features: Expected number of features
        Raises:
            ValueError: If matrix is invalid
        """
        if not corr_coeffs:
            raise ValueError("Correlation matrix cannot be None for multiple features")
        if len(corr_coeffs) != n_features:
            raise ValueError(f"Correlation matrix must be {n_features}x{n_features}, got {len(corr_coeffs)} rows")
        for i, row in enumerate(corr_coeffs):
            if len(row) != n_features:
                raise ValueError(f"Correlation matrix row {i} has invalid length: {len(row)}, expected {n_features}")

        corr_array = np.array(corr_coeffs)
        
        if not np.allclose(corr_array, corr_array.T):
            raise ValueError("Correlation matrix must be symmetric")
        if not np.allclose(np.diag(corr_array), 1.0):
            raise ValueError("Correlation matrix diagonal must be all ones")
        if np.any(np.abs(corr_array) > 1.0):
            raise ValueError("All correlation coefficients must be between -1 and 1")
        if np.any(np.linalg.eigvals(corr_array) < -1e-10):
            raise ValueError("Correlation matrix must be positive semi-definite")