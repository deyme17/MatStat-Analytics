import numpy as np
from models.homogens.base_homogen_test import BaseHomogenTest
from scipy import stats


class MultiNormalTest(BaseHomogenTest):
    """
    Multivariate normality homogeneity test for k n-dimensional samples.
      1. H0: DC{ksi_1} = DC{ksi_2} = ... = DC{ksi_k}  (equal covariance matrices)
      2. H0: E{ksi_1} = E{ksi_2} = ... = E{ksi_k}     (equal mean vectors)
    """
    def name(self) -> str:
        """
        Returns: "Multivariate Normality Test".
        """
        return "Multivariate Normality Test"
    
    def run(self, samples: list[np.ndarray], alpha: float = 0.05, is_independent: bool = True) -> dict:
        """Run the multivariate normality test for n samples.
        Args:
            samples (list[np.ndarray]): List of n samples, each as a numpy array (2D for multivariate).
            alpha (float): Significance level for the test.
            is_independent (bool): Whether the samples are independent (not used in this test).
        Returns:
            dict: {
                "cov_statistic": float,
                "cov_critical": float,
                "cov_df": int,
                "cov_p_value": float,
                "cov_decision": bool,
                "mean_statistic": float,
                "mean_critical": float,
                "mean_df": int,
                "mean_p_value": float,
                "mean_decision": bool,
                "decision": bool,
            }
        """
        if len(samples) < 2 or not is_independent: return {}
        samples = [np.atleast_2d(s) if s.ndim == 1 else s for s in samples]

        k = len(samples)
        n = samples[0].shape[1]
        
        # perform covariance equality test
        cov_result = self._test_covariance_equality(samples, k, n, alpha)
        # perform mean equality test 
        if cov_result["decision"]:
            if k == 2:
                mean_result = self._test_means_equal_dc(
                    samples[0], samples[1], n, alpha
                )
            else:
                mean_result = self._test_means_unequal_dc(samples, k, n, alpha)
        else:
            mean_result = self._test_means_unequal_dc(samples, k, n, alpha)

        # result
        overall_decision = cov_result["decision"] and mean_result["decision"]
        return {
            "cov_statistic":    cov_result["statistic"],
            "cov_critical":     cov_result["chi2_critical"],
            "cov_df":           cov_result["df"],
            "cov_p_value":      cov_result["p_value"],
            "cov_decision":     cov_result["decision"],
            "mean_statistic":   mean_result["statistic"],
            "mean_critical":    mean_result["chi2_critical"],
            "mean_df":          mean_result["df"],
            "mean_p_value":     mean_result["p_value"],
            "mean_decision":    mean_result["decision"],
            "decision":         bool(overall_decision),
        }

    def _test_covariance_equality(self, samples: list[np.ndarray], k: int, n: int, alpha: float = 0.05) -> dict:
        """
        Test hypothesis of equal covariance matrices.
        """
        N_d = np.array([s.shape[0] for s in samples])
        N = N_d.sum()

        S_d = [np.cov(s, rowvar=False) for s in samples]                # covariance matrices
        S = 1 / (N - k) * sum((N_d[d] -1) * S_d[d] for d in range(k))   # pooled covariance matrix
        ln_S = np.log(np.linalg.det(S) + 1e-10)

        V = sum(((N_d[d] - 1) / 2) * (np.log(ln_S / np.linalg.det(S_d[d]) + 1e-10))
                                                                 for d in range(k))
        df = n * (n + 1) * (k - 1) // 2
        chi2_crit = stats.chi2.ppf(1 - alpha, df)
        p_value = float(1 - stats.chi2.cdf(V, df))
        decision = bool(V <= chi2_crit)
 
        return {
            "statistic": float(V),
            "chi2_critical": float(chi2_crit),
            "df": df,
            "p_value": p_value,
            "decision": decision,
        }

    def _test_means_unequal_dc(self, samples: list[np.ndarray], k: int, n: int, alpha: float = 0.05) -> dict:
        """
        Test hypothesis of equal means without assuming equal covariances (unequal DC).
        """
        N_d = np.array([s.shape[0] for s in samples])

        x_bar_d = [s.mean(axis=0) for s in samples]                     # mean vectors
        S_d = [np.cov(s, rowvar=False) for i, s in enumerate(samples)]  # covariance matrices
        S_d_inv = [np.linalg.inv(S) for S in S_d]                       # inverse covariance matrices

        A = sum(N_d[d] * S_d_inv[d] for d in range(k))
        b = sum(N_d[d] * S_d_inv[d] @ x_bar_d[d] for d in range(k))
        x_bar = np.linalg.solve(A, b)                                   # pooled mean vector

        # V statistic
        V = sum(N_d[d] * (x_bar_d[d] - x_bar).T @ S_d_inv[d] @ (x_bar_d[d] - x_bar)
                                                                 for d in range(k))
        df = n * (k - 1)
        chi2_crit = stats.chi2.ppf(1 - alpha, df)
        p_value = 1 - stats.chi2.cdf(V, df)
        decision = V <= chi2_crit

        return {
            "statistic": float(V),
            "chi2_critical": float(chi2_crit),
            "df": df,
            "p_value": float(p_value),
            "decision": decision
        }

    def _test_means_equal_dc(self, x: np.ndarray, y: np.ndarray, n: int, alpha: float = 0.05) -> dict:
        """
        Test hypothesis of equal mean vectors assuming equal covariance matrices (equal DC).
        """
        N1, N2 = x.shape[0], y.shape[0]

        S0 = self._compute_s0(x, y, N1, N2, n)
        S1 = self._compute_s1(x, y, N1, N2, n)
        V = -(N1 + N2 - 2 - n/2) * np.log(np.linalg.det(S1) / (np.linalg.det(S0) + 1e-10))

        df = n * (n + 1) // 2
        chi2_crit = stats.chi2.ppf(1 - alpha, df)
        p_value = 1 - stats.chi2.cdf(V, df)
        decision = V <= chi2_crit

        return {
            "statistic": float(V),
            "chi2_critical": float(chi2_crit),
            "df": df,
            "p_value": float(p_value),
            "decision": decision
        }

    def _compute_s0(self, x: np.ndarray, y: np.ndarray, N1: int, N2: int, n: int) -> np.ndarray:
        """
        S0 elements - both samples treated as one (assumes equal means).
        """
        denom = N1 + N2 - 2
        S0 = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                xx = np.dot(x[:, i], x[:, j]) + np.dot(y[:, i], y[:, j])
                cross = (x[:, i].sum() + y[:, i].sum()) * \
                        (x[:, j].sum() + y[:, j].sum()) / (N1 + N2)
                S0[i, j] = (xx - cross) / denom
        return S0
 
    def _compute_s1(self, x: np.ndarray, y: np.ndarray, N1: int, N2: int, n: int) -> np.ndarray:
        """
        S1 elements - separate means (means may differ).
        """
        denom = N1 + N2 - 2
        S1 = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                xx = np.dot(x[:, i], x[:, j]) + np.dot(y[:, i], y[:, j])
                cross = (x[:, i].sum() * x[:, j].sum() / N1 +
                         y[:, i].sum() * y[:, j].sum() / N2)
                S1[i, j] = (xx - cross) / denom
        return S1