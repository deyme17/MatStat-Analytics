from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QHBoxLayout
import pandas as pd
from typing import List, Type
from models.stat_distributions.stat_distribution import StatisticalDistribution
from services.analysis_services.gof_register import GOFService
from views.widgets.hypoteswidgets.gof_test_panel import BaseTestPanel


class GOFTestTab(QWidget):
    """
    A tab widget for evaluating Goodness-of-Fit (GOF) tests.
    """

    def __init__(self, context, graph_panel, gof_service: GOFService, test_panels: List[Type[BaseTestPanel]]) -> None:
        """
        Initialize the GOF test tab.

        Args:
            context (AppContext): Application context container
            graph_panel: Object with get_selected_distribution().
            gof_service (GOFService): Service to perform GOF tests.
            test_panels (list): List of GOF test panel classes (not instances).
        """
        super().__init__()
        self.data_model = context.data_model
        self.graph_panel = graph_panel

        self.test_panels: List[BaseTestPanel] = [panel(gof_service) for panel in test_panels]

        self.alpha_spinbox = QDoubleSpinBox()
        self.alpha_spinbox.setRange(0.01, 0.99)
        self.alpha_spinbox.setSingleStep(0.01)
        self.alpha_spinbox.setDecimals(2)
        self.alpha_spinbox.setValue(0.05)
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
        dist: StatisticalDistribution = self.graph_panel.get_selected_distribution()
        model = self.data_model

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