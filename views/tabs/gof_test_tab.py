from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QHBoxLayout
from views.widgets.hypoteswidgets.gof_test_panel import BaseTestPanel

ALPHA_MIN, ALPHA_MAX = 0.01, 0.99
ALPHA_STEP = 0.1
ALPHA_PRECISION = 2
DEFAULT_ALPHA = 0.05

class GOFTestTab(QWidget):
    """
    A tab widget for evaluating Goodness-of-Fit (GOF) tests.
    """
    def __init__(self, get_data_model, get_dist_func, gof_controller, test_panels: list[BaseTestPanel]) -> None:
        """
        Args:
            get_data_model: Function for getting current data model.
            get_dist_func: Function for getting current selected distribution.
            gof_controller (GOFController): Controller to perform GOF tests.
            test_panels (list): List of GOF test panel classes (not instances).
        """
        super().__init__()
        self.get_data_model = get_data_model
        self.get_dist_func = get_dist_func
        self.test_panels: list[BaseTestPanel] = [panel(gof_controller) for panel in test_panels]

        self.alpha_spinbox = QDoubleSpinBox()
        self.alpha_spinbox.setRange(ALPHA_MIN, ALPHA_MAX)
        self.alpha_spinbox.setSingleStep(ALPHA_STEP)
        self.alpha_spinbox.setDecimals(ALPHA_PRECISION)
        self.alpha_spinbox.setValue(DEFAULT_ALPHA)
        self.alpha_spinbox.valueChanged.connect(self.evaluate_tests)

        # Alpha layout
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Significance level α:"))
        alpha_layout.addWidget(self.alpha_spinbox)
        alpha_layout.addStretch()

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(alpha_layout)
        for panel in self.test_panels:
            layout.addWidget(panel)
        layout.addStretch()
        self.setLayout(layout)

    def evaluate_tests(self) -> None:
        """
        Evaluates all GOF tests based on current data and selected distribution.
        """
        dist = self.get_dist_func()
        model = self.get_data_model()

        if dist is None or model is None or model.series.empty:
            return

        data = model.series.dropna()
        if data.empty:
            return

        alpha = self.alpha_spinbox.value()
        for test in self.test_panels:
            test.evaluate(data, dist, alpha)

    def clear_panels(self) -> None:
        """
        Clears all hypothesis test panels.
        """
        for test in self.test_panels:
            test.clear()