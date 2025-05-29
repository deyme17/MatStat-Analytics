import numpy as np

class SimulationService:
    @staticmethod
    def generate_sample(distribution, size, params):
        """
        Generate a sample from the specified distribution using the inverse CDF method.

        :param distribution: An instance of a class that implements get_inverse_cdf(x, params).
        :param size: Number of values to generate.
        :param params: Parameters to pass to the distribution's inverse CDF.
        :return: np.ndarray of simulated values.
        """
        u = np.random.uniform(0, 1, size)
        return distribution.get_inverse_cdf(u, params)
    
    @staticmethod
    def run_experiment(distribution, sizes, n_repeat, true_mean, params):
        """
        Run a simulation experiment using T-tests on generated samples.

        :param distribution: Distribution strategy instance.
        :param sizes: List of sample sizes.
        :param n_repeat: Number of repetitions per sample size.
        :param true_mean: The true mean to test against.
        :param params: Parameters for the distribution.
        :return: List of dicts with size, mean of t-statistics, std of t-statistics.
        """
        from services.analysis_services.statistics_service import StatisticsService

        results = []

        for size in sizes:
            t_stats = []
            for _ in range(n_repeat):
                sample = SimulationService.generate_sample(distribution, size, params)
                t_result = StatisticsService.perform_t_test(sample, true_mean=true_mean)
                t_stats.append(t_result['t_statistic'])

            mean_t = np.mean(t_stats)
            std_t = np.std(t_stats, ddof=1)
            results.append({
                'size': size,
                't_mean': mean_t,
                't_std': std_t
            })

        return results