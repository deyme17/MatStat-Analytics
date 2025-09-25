from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class SignCriterionPanel(BaseHomoTestPanel):
    """
    Panel for Sign criterion test (paired samples).
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "S_statistic", "label": "S-statistic"},
            {"key": "alpha0", "label": "α₀"},
            {"key": "S_star", "label": "S*"},
            {"key": "shift_val_theta", "label": "Shift θ value"}
        ]
        super().__init__(homogen_controller, stats, 2, False)

    def get_test_name(self) -> str:
        return "sign criterion test"