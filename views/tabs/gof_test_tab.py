from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QHBoxLayout
from views.widgets.hypoteswidgets.pearson_panel import PearsonChi2Panel
from views.widgets.hypoteswidgets.ks_panel import KolmogorovSmirnovPanel

class GOFTestTab(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.pearson_panel = PearsonChi2Panel(window)
        self.ks_panel = KolmogorovSmirnovPanel(window)

        self.alpha_spinbox = QDoubleSpinBox()
        self.alpha_spinbox.setRange(0.01, 0.99)
        self.alpha_spinbox.setSingleStep(0.01)
        self.alpha_spinbox.setDecimals(2)
        self.alpha_spinbox.setValue(0.05)
        self.alpha_spinbox.valueChanged.connect(self.evaluate_tests)

        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Significance level α:"))
        alpha_layout.addWidget(self.alpha_spinbox)
        alpha_layout.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(alpha_layout)
        layout.addWidget(self.pearson_panel)
        layout.addWidget(self.ks_panel)
        layout.addStretch()
        self.setLayout(layout)

    def evaluate_tests(self):
        dist = self.window.graph_panel.get_selected_distribution()
        model = self.window.data_model

        if dist is None or model is None or model.series.empty:
            return

        data = model.series.dropna()
        if data.empty:
            return

        alpha = self.alpha_spinbox.value()
        self.pearson_panel.evaluate(data, dist, alpha)
        self.ks_panel.evaluate(data, dist, alpha)

    def clear_tests(self):
        self.pearson_panel.clear()
        self.ks_panel.clear()