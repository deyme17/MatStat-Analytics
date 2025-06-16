from PyQt6.QtWidgets import QLabel
import pandas as pd
from views.widgets.hypoteswidgets.gof_test_panel import BaseTestPanel
from services.analysis_services.gof_register import GOFService
from models.stat_distributions.stat_distribution import StatisticalDistribution


class KolmogorovSmirnovPanel(BaseTestPanel):
    """
    Panel for Kolmogorov–Smirnov GOF test with detailed stats.
    """

    def __init__(self, gof_service: GOFService) -> None:
        """
        Initialize the Kolmogorov–Smirnov test panel.

        Args:
            gof_service (GOFService): Service to perform the test.
        """
        super().__init__("Kolmogorov–Smirnov Test", gof_service)

        self.dn_label: QLabel = self.add_stat_label("Statistic (Dₙ): ")
        self.z_label: QLabel = self.add_stat_label("z = √n * Dₙ: ")
        self.critical_label: QLabel = self.add_stat_label("Critical z: ")
        self.p_label: QLabel = self.add_stat_label("P(z): ")

        self.finalize_layout()

    def evaluate(self, data: pd.Series, dist: StatisticalDistribution, alpha: float) -> None:
        """
        Perform Kolmogorov–Smirnov test and update panel.

        Args:
            data (pd.Series): Sample data to test.
            dist (StatisticalDistribution): Fitted distribution.
            alpha (float): Significance level.
        """
        result = self.gof_service.perform_ks_test(data, dist, alpha)
        if result is None:
            self.clear()
            return

        self.dn_label.setText(f"Statistic (Dₙ): {result.statistic:.4f}")
        self.z_label.setText(f"z = √n * Dₙ: {result.z_value:.4f}")
        self.critical_label.setText(f"Critical z: {result.critical:.4f}")
        self.p_label.setText(f"P(z): {result.p_value:.4f}")

        self.update_result(result.passed)