from PyQt6.QtWidgets import QLabel
from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel
import pandas as pd

class NormalHomogenPanel(BaseHomoTestPanel):
    """
    Panel for Normal Homogeneity test with detailed statistics for variance and mean comparison.
    """
    def __init__(self, homogen_controller) -> None:
        """
        Initialize the Normal Homogeneity test panel.
        Args:
            homogen_controller (HomogenController): Controller for computing test values.
        """
        super().__init__(homogen_controller)
        
        # f test
        self.f_statistic_label: QLabel = self.add_stat_label("F-statistic: ")
        self.p_value_var_label: QLabel = self.add_stat_label("P-value (variance): ")
        self.var_consistent_label: QLabel = self.add_stat_label("Variance consistency: ")
        
        # t-test 
        self.t_statistic_label: QLabel = self.add_stat_label("t-statistic: ")
        self.p_value_mean_label: QLabel = self.add_stat_label("P-value (mean): ")
        self.mean_consistent_label: QLabel = self.add_stat_label("Mean consistency: ")
        
        self.test_type_label: QLabel = self.add_stat_label("Test type: ")

        self.finalize_layout()

    def get_test_name(self) -> str:
        """
        Get the name of the test for identification.
        Returns:
            str: Name of the normal homogeneity test.
        """
        return "normal homogeneity test"

    def evaluate(self, samples: list[pd.Series], alpha: float, is_independent: bool) -> None:
        """
        Evaluate the Normal Homogeneity test for two samples.
        Args:
            samples (list[pd.Series]): List of samples to test (should contain exactly 2 samples).
            alpha (float): Significance level.
            is_independent (bool): True if samples are independent, False if paired.
        """
        if len(samples) != 2:
            self.clear()
            return
            
        result = self.homogen_controller.run_2samples_test(
            test_name=self.get_test_name(),
            samples=samples,
            alpha=alpha,
            is_independent=is_independent
        )
        
        if result is None or not result:
            self.clear()
            return

        # update results
        if result.get('f_statistic') is not None:
            self.f_statistic_label.setText(f"F-statistic: {result['f_statistic']:.4f}")
            self.p_value_var_label.setText(f"P-value (variance): {result['p_value_var']:.4f}")
            self.var_consistent_label.setText(
                f"Variance consistency: {'Yes' if result['var_consistent'] else 'No'}"
            )
        else:
            self.f_statistic_label.setText("F-statistic: N/A (paired samples)")
            self.p_value_var_label.setText("P-value (variance): N/A")
            self.var_consistent_label.setText("Variance consistency: N/A")

        self.t_statistic_label.setText(f"t-statistic: {result['t_statistic']:.4f}")
        self.p_value_mean_label.setText(f"P-value (mean): {result['p_value_mean']:.4f}")
        self.mean_consistent_label.setText(
            f"Mean consistency: {'Yes' if result['mean_consistent'] else 'No'}"
        )
        
        self.test_type_label.setText(f"Test type: {result['type']}")
        self.update_result(result['decision'])

    def clear(self) -> None:
        """
        Reset the panel to the default untested state.
        """
        super().clear()
        self.f_statistic_label.setText("F-statistic: ")
        self.p_value_var_label.setText("P-value (variance): ")
        self.var_consistent_label.setText("Variance consistency: ")
        self.t_statistic_label.setText("t-statistic: ")
        self.p_value_mean_label.setText("P-value (mean): ")
        self.mean_consistent_label.setText("Mean consistency: ")
        self.test_type_label.setText("Test type: ")