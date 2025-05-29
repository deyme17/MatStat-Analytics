from PyQt6.QtWidgets import QLabel
from views.widgets.hypoteswidgets.gof_test_panel import BaseTestPanel
from services.analysis_services.gof_register import GOFService

class PearsonChi2Panel(BaseTestPanel):
    """
    A panel widget for displaying the results of Pearson's chi-squared goodness-of-fit test.
    
    Inherits from:
        BaseTestPanel: Base class providing layout and result formatting logic.

    Attributes:
        statistic_label (QLabel): Displays the chi-squared test statistic.
        df_label (QLabel): Displays the degrees of freedom used in the test.
        critical_value_label (QLabel): Displays the critical chi-squared value at a given α level.
        p_value_label (QLabel): Displays the p-value associated with the test statistic.
    """

    def __init__(self, window):
        """
        Initialize the PearsonChi2Panel with labeled result fields.

        Args:
            window (QMainWindow): The main application window (used for accessing UI components).
        """
        super().__init__("Pearson's χ² Test", window)

        self.statistic_label = self.add_stat_label("χ²: ")
        self.df_label = self.add_stat_label("Degrees of freedom: ")
        self.critical_value_label = self.add_stat_label("χ²(α, df): ")
        self.p_value_label = self.add_stat_label("P(χ² ≤ x): ")

        self.finalize_layout()

    def evaluate(self, data, dist, alpha):
        """
        Evaluate the chi-squared test for the given data and distribution.

        Args:
            data (pd.Series): Input data to test.
            dist (StatisticalDistribution): The theoretical distribution to test against.
            alpha (float): Significance level for the test.

        Behavior:
            - Updates labels with the statistic, degrees of freedom, critical value, and p-value.
            - Calls `update_result(True|False)` depending on the test outcome.
            - Handles and displays exceptions if the test fails.
        """
        try:
            bins = self.window.graph_panel.bins_spinbox.value()
            result = GOFService.run_tests(data, dist, bins=bins, alpha=alpha)["chi2"]
            extra = result.get("extra", {})

            self.statistic_label.setText(f"χ²: {result['statistic']:.4f}")
            self.df_label.setText(f"Degrees of freedom: {extra.get('df', 0)}")
            self.critical_value_label.setText(
                f"χ²(α={alpha:.2f}, df={extra.get('df', 0)}): {extra.get('critical_value', 0):.4f}"
            )
            self.p_value_label.setText(f"P(χ² ≤ x): {result['p_value']:.4f}")
            self.update_result(result["passed"])
        except Exception as e:
            self.statistic_label.setText(f"Error: {str(e)}")

    def clear(self):
        """
        Clear all labels to default state and reset the test result display.
        """
        self.statistic_label.setText("χ²: ")
        self.df_label.setText("Degrees of freedom: ")
        self.critical_value_label.setText("χ²(α, df): ")
        self.p_value_label.setText("P(χ² ≤ x): ")
        super().clear()
