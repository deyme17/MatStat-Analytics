from PyQt6.QtWidgets import QWidget
from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel


class HomogenTab(QWidget):
    """
    A tab widget for evaluating Homogenity tests.
    """
    def __init__(self, get_data_model, homogen_controller, homogen_panels: list[BaseHomoTestPanel]) -> None:
        """
        Args:
            get_data_model: Function for getting current data model.
            homogen_controller (HomogenController): Controller to perform Homogenity tests.
            homogen_panels (list): List of Homogenity test panel classes (not instances).
        """
        super().__init__()
        self.get_data_model = get_data_model
        self.homogen_controller = homogen_controller
        self.homogen_panels: list[BaseHomoTestPanel] = [panel(homogen_controller) for panel in homogen_panels]
        ...