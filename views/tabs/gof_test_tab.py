from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QHBoxLayout
from views.widgets.hypoteswidgets.pearson_panel import PearsonChi2Panel
from views.widgets.hypoteswidgets.ks_panel import KolmogorovSmirnovPanel

class GOFTestTab(QWidget):
    """
    A tab widget for evaluating Goodness-of-Fit (GOF) tests.
    """

    def __init__(self, window):
        super().__init__()
        self.window = window

        # Initialize GOF test panels
        self.tests = [
            PearsonChi2Panel(window),
            KolmogorovSmirnovPanel(window)
        ]

        # Significance level selector
        self.alpha_spinbox = QDoubleSpinBox()
        self.alpha_spinbox.setRange(0.01, 0.99)
        self.alpha_spinbox.setSingleStep(0.01)
        self.alpha_spinbox.setDecimals(2)
        self.alpha_spinbox.setValue(0.05)
        self.alpha_spinbox.valueChanged.connect(self.evaluate_tests)

        # Layout for alpha selector
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Significance level α:"))
        alpha_layout.addWidget(self.alpha_spinbox)
        alpha_layout.addStretch()

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(alpha_layout)
        for panel in self.tests:
            layout.addWidget(panel)
        layout.addStretch()
        self.setLayout(layout)

    def evaluate_tests(self):
        """
        Evaluates all registered GOF test panels based on the current data and 
        selected distribution. Triggered when the significance level is changed 
        or when the distribution is updated.
        """
        dist = self.window.graph_panel.get_selected_distribution()
        model = self.window.data_model

        if dist is None or model is None or model.series.empty:
            return

        data = model.series.dropna()
        if data.empty:
            return

        alpha = self.alpha_spinbox.value()
        for test in self.tests:
            test.evaluate(data, dist, alpha)

    def clear_tests(self):
        """
        Clears the results of all GOF test panels.
        """
        for test in self.tests:
            test.clear()
