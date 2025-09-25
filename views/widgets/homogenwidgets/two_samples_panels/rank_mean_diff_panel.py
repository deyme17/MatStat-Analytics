from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class RankMeanDiffPanel(BaseHomoTestPanel):
    """
    Panel for Rank Mean Difference test.
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "v_statistic", "label": "v-statistic"},
            {"key": "xi2_crit", "label": "Critical χ²"},
            {"key": "p_value", "label": "P-value"}
        ]
        super().__init__(homogen_controller, stats, 2, True)

    def get_test_name(self) -> str:
        return "Rank Mean Difference test"