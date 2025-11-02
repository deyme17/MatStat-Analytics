from PyQt6.QtWidgets import QLabel
import pandas as pd
from views.widgets.gofwidgets.gof_test_panel import BaseTestPanel
from models.stat_distributions.stat_distribution import StatisticalDistribution


class Pearson2DNormalPanel(BaseTestPanel):
    """
    Panel for 2D Normal Chi-Squared GOF test with detailed stats.
    """
    def __init__(self, gof_controller) -> None:
        """
        Initialize the 2D Normal χ² test panel.
        Args:
            gof_controller (GOFController): Controller for computing test values.
        """
        super().__init__("2D Normal Chi² Test", gof_controller)
        self.note: QLabel = self.add_stat_label("! Note: Test only 2D data for normality")
        self.statistic_label: QLabel = self.add_stat_label("χ²: ")
        self.df_label: QLabel = self.add_stat_label("Degrees of freedom: ")
        self.critical_value_label: QLabel = self.add_stat_label("χ²(α, df): ")
        self.p_value_label: QLabel = self.add_stat_label("P(χ² ≤ x): ")
        self.expected_range_label: QLabel = self.add_stat_label("Expected freq range: ")

        self.finalize_layout()

    def evaluate(self, data: pd.DataFrame, dist: StatisticalDistribution, alpha: float) -> None:
        """
        Evaluate the 2D Normal chi-squared test.
        Args:
            data (pd.DataFrame): Observed 2D data sample (must have 2 columns).
            dist (StatisticalDistribution): Not used for this test (parameters estimated from data).
            alpha (float): Significance level.
        """
        result = self.gof_controller.run_test('norm2d_chi2', data, dist, alpha)
        if result is None:
            self.clear()
            return

        self.statistic_label.setText(f"χ²: {result['statistic']:.4f}")
        self.df_label.setText(f"Degrees of freedom: {result['extra']['df']}")
        self.critical_value_label.setText(f"χ²(α, df): {result['extra']['critical_value']:.4f}")
        self.p_value_label.setText(f"P(χ² ≤ x): {result['p_value']:.4f}")
        
        exp_min = result['extra']['expected_min']
        exp_max = result['extra']['expected_max']
        self.expected_range_label.setText(f"Expected freq range: [{exp_min:.2f}, {exp_max:.2f}]")

        self.update_result(result['passed'])