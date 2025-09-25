from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class SignsCriterionPanel(BaseHomoTestPanel):
    """
    Panel for Signs criterion test (paired samples).
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "S_statistic", "label": "S-statistic"},
            {"key": "alpha0", "label": "α₀"},
            {"key": "S_star", "label": "S*"},
            {"key": "z_crit", "label": "Critical z"},
            {"key": "p_value", "label": "P-value"},
            {"key": "shift_val_theta", "label": "Shift θ value"}
        ]
        super().__init__(homogen_controller, stats, 2, False)

    def get_test_name(self) -> str:
        return "Signs Criterion test"