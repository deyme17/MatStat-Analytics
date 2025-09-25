import numpy as np
from scipy.stats import f, t
from models.homogens.base_homogen_test import BaseHomogenTest


class NormalHomogenTest(BaseHomogenTest):
    """Homogeneity test for Normal-distributed data."""

    def name(self) -> str:
        """
        Returns: "normal homogeneity test"
        """
        return "normal homogeneity test"

    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = False) -> dict:
        """
        Perform the homogeneity test for two samples of normal-distributed datas.
        Check the variance and mean coincidence.
        Args:
            samples: two input data arrays
            alpha: significance level
            is_independent: True if samples is independent else False
        Returns:
            dictionary with test results {f_statistic or None, var_consistent or None, p_value_var or None, 
                                        t_statistic, mean_consistent, p_value_mean, decision, independent}
        """
        if len(samples) != 2: return {}

        # stats
        f_stat, p_value_var, is_var_consident = None, None, None
        t_stat, p_value_mean, is_mean_consident = None, None, None

        x, y, = samples
        n1, n2 = len(x), len(y)

        # check the variance coincidence
        f_stat, p_value_var, is_var_consident = self._perform_variance_concidence(x, y, n1, n2, alpha, is_independent)
        # check the variance coincidence
        t_stat, p_value_mean, is_mean_consident = self._perform_mean_concidence(x, y, n1, n2, alpha, is_independent)

        return {
            "f_statistic": f_stat,
            "var_consistent": is_var_consident,
            "p_value_var": p_value_var,

            "t_statistic": t_stat,
            "mean_consistent": is_mean_consident,
            "p_value_mean": p_value_mean,

            "decision": (is_var_consident and is_mean_consident) if is_independent else False,
        }

    def _perform_variance_concidence(self, x: np.ndarray, y: np.ndarray, n1: int, n2: int, 
                                     alpha: float = 0.05, is_independent: bool = False) -> tuple[float, float, bool]:
        """
        Check the variance coincidence (Fisher's F-test) for two samples.
        Args:
            x, y: two samples
            n1, n2: the length of samples
            alpha: significance level
            is_independent: True if independent samples, False if paired
        Returns:
            t_stat: calculated t-statistic
            p_value: p-value of the test
            is_consistent: True if means are not significantly different
        """
        if not is_independent: 
            return None, None, None

        s1, s2 = np.var(x, ddof=1), np.var(y, ddof=1)

        if s1 >= s2:
            f_stat = s1 / s2
            v1, v2 = n1 - 1, n2 - 1
        else:
            f_stat = s2 / s1
            v1, v2 = n2 - 1, n1 - 1

        p_value = 2 * min(f.cdf(f_stat, v1, v2), 1 - f.cdf(f_stat, v1, v2))
        is_consistent = p_value > alpha

        return f_stat, p_value, is_consistent

    def _perform_mean_concidence(self, x: np.ndarray, y: np.ndarray, n1: int, n2: int, 
                                 alpha: float = 0.05, is_independent: bool = False) -> tuple[float, float, bool]:
        """
        Check the mean coincidence (Student's t-test) for two samples.
        Args:
            x, y: two samples
            n1, n2: the length of samples
            alpha: significance level
            is_independent: True if independent samples, False if paired
        Returns:
            t_stat: calculated t-statistic
            p_value: p-value of the test
            is_consistent: True if means are not significantly different
        """
        # dependent
        if not is_independent:
            d = x - y
            std_d = np.std(d, ddof=1)

            if std_d == 0 or len(d) <= 1:
                t_stat = 0.0
                p_value = 1.0
            else:
                t_stat = np.mean(d) / (std_d / np.sqrt(len(d)))
                df = len(d) - 1
                p_value = 2 * (1 - t.cdf(abs(t_stat), df=df))

            is_consistent = p_value > alpha
            return t_stat, p_value, is_consistent

        # independent
        if n1 + n2 <= 25:
            s_pooled = ((n1 - 1) * np.var(x, ddof=1) + (n2 - 1) * np.var(y, ddof=1)) / (n1 + n2 - 2)
            t_stat = (np.mean(x) - np.mean(y)) / np.sqrt(s_pooled * (1/n1 + 1/n2))
            df = n1 + n2 - 2
        else:
            Sx2, Sy2 = np.var(x, ddof=1), np.var(y, ddof=1)
            S_diff = np.sqrt(Sx2 / n1 + Sy2 / n2)
            t_stat = (np.mean(x) - np.mean(y)) / S_diff
            df = n1 + n2 - 2

        p_value = 2 * (1 - t.cdf(abs(t_stat), df=df))
        is_consistent = p_value > alpha

        return t_stat, p_value, is_consistent