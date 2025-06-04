from PyQt6.QtWidgets import QLabel
from views.widgets.hypoteswidgets.gof_test_panel import BaseTestPanel
from services.analysis_services.gof_register import GOFService

class KolmogorovSmirnovPanel(BaseTestPanel):
    """
    A widget panel for displaying the results of the Kolmogorov-Smirnov goodness-of-fit test.

    Inherits:
        BaseTestPanel: Provides layout and UI behavior for hypothesis test result panels.

    Attributes:
        dn_label (QLabel): Displays the Dₙ statistic.
        z_label (QLabel): Displays the z-score calculated as √n * Dₙ.
        critical_label (QLabel): Displays the critical z value based on the chosen alpha.
        p_label (QLabel): Displays the p-value for the test.
    """

    def __init__(self, window):
        """
        Initializes the panel with labeled fields for KS test results.

        Args:
            window (QMainWindow): Reference to the main application window.
        """
        super().__init__("Refined Kolmogorov Test", window)

        self.dn_label = self.add_stat_label("Statistic (Dₙ): ")
        self.z_label = self.add_stat_label("z = √n * Dₙ: ")
        self.critical_label = self.add_stat_label("Critical z: ")
        self.p_label = self.add_stat_label("P(z): ")

        self.finalize_layout()

    def evaluate(self, data, dist, alpha):
        """
        Executes the KS test on provided data and updates the UI with test results.

        Args:
            data (pd.Series): The dataset to evaluate.
            dist (StatisticalDistribution): The theoretical distribution to test against.
            alpha (float): The significance level (e.g., 0.05).

        Behavior:
            - Calls the GOFService to perform the KS test.
            - Displays Dₙ, z-statistic, critical value, and p-value.
            - Highlights the result depending on whether the null hypothesis is accepted.
        """
        try:
            result = GOFService.run_tests(data, dist, alpha=alpha)["ks"]
            extra = result.get("extra", {})

            self.dn_label.setText(f"Statistic (Dₙ): {result['statistic']:.4f}")
            self.z_label.setText(f"z = √n * Dₙ: {extra.get('z_stat', 0):.4f}")
            self.critical_label.setText(f"Critical z(α={alpha:.2f}): {extra.get('critical_value', 0):.4f}")
            self.p_label.setText(f"P(z): {result['p_value']:.4f}")
            self.update_result(result["passed"])
        except Exception as e:
            self.dn_label.setText(f"Error: {str(e)}")

    def clear(self):
        """
        Resets all displayed values to their initial state.
        """
        self.dn_label.setText("Statistic (Dₙ): ")
        self.z_label.setText("z = √n * Dₙ: ")
        self.critical_label.setText("Critical z: ")
        self.p_label.setText("P(z): ")
        super().clear()
