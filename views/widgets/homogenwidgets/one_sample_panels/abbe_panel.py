from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class AbbePanel(BaseHomoTestPanel):
    """
    Panel for AbbePanel test (one sample) for independancy checking.
    Displays test statistic and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "d_statistic", "label": "d-statistic"},
            {"key": "q_statistic", "label": "q-statistic"},
            {"key": "E[q]", "label": "Expected value ofq"},
            {"key": "D[q]", "label": "Variance of q"},
            {"key": "U_statistic", "label": "U-statistic"},
            {"key": "p_value", "label": "P-value"}
        ]
        super().__init__(homogen_controller, stats, 1, None)

    def get_test_name(self) -> str:
        return "abbe test"