from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class NormalHomogenPanel(BaseHomoTestPanel):
    """
    Panel for Normal Homogeneity test with detailed statistics for variance and mean comparison.
    """
    def __init__(self, homogen_controller) -> None:
        stats = [
            {"key": "f_statistic", "label": "F-statistic"},
            {"key": "p_value_var", "label": "P-value (variance)"},
            {"key": "var_consistent", "label": "Variance consistency"},
            {"key": "t_statistic", "label": "t-statistic"},
            {"key": "p_value_mean", "label": "P-value (mean)"},
            {"key": "mean_consistent", "label": "Mean consistency"},
        ]
        super().__init__(homogen_controller, stats, 2, None)

    def get_test_name(self) -> str:
        return "Normal Homogeneity test"