from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel

class HPanel(BaseHomoTestPanel):
    """
    Panel for H test.
    Displays test statistic, p-value, and decision.
    """
    def __init__(self, homogen_controller):
        stats = [
            {"key": "", "label": ""},
        ]
        super().__init__(homogen_controller, stats, None, True)

    def get_test_name(self) -> str:
        return "H test"