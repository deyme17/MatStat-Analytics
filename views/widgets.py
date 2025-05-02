from PyQt6.QtWidgets import QGroupBox, QGridLayout, QRadioButton, QButtonGroup, QLabel, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.ui_styles import groupMargin
from models.stat_distributions import (
    NormalDistribution, ExponentialDistribution,
    UniformDistribution, WeibullDistribution, LaplaceDistribution
)

class DistributionWidget(QGroupBox):
    def __init__(self, on_change=None, parent=None):
        super().__init__("Statistical Distributions", parent)
        self.setMaximumHeight(100)
        self.setStyleSheet(groupMargin)

        self.distribution_map = {
            "Normal": NormalDistribution,
            "Exponential": ExponentialDistribution,
            "Uniform": UniformDistribution,
            "Weibull": WeibullDistribution,
            "Laplace": LaplaceDistribution
        }

        self.button_group = QButtonGroup(self)
        layout = QGridLayout()

        for index, (name, dist_cls) in enumerate(self.distribution_map.items()):
            btn = QRadioButton(name)
            self.button_group.addButton(btn)
            layout.addWidget(btn, index // 3, index % 3)
            if on_change:
                btn.toggled.connect(on_change)

        self.setLayout(layout)

    def get_selected_distribution(self):
        btn = self.button_group.checkedButton()
        if btn:
            dist_class = self.distribution_map.get(btn.text())
            if dist_class:
                return dist_class()
        return None


def create_test_group(test_names):
    group = QGroupBox("Goodness-of-fit Tests")
    layout = QGridLayout()
    group.setStyleSheet(groupMargin)
    layout.setContentsMargins(10, 25, 10, 10)

    test_labels = {}
    for index, test_name in enumerate(test_names):
        label = QLabel(f"{test_name}:")
        value = QLabel("statistic: , p-value: ")
        layout.addWidget(label, index, 0)
        layout.addWidget(value, index, 1)
        test_labels[test_name] = value

    group.setLayout(layout)
    return group, test_labels


def create_graph_widgets(graph_names):
    tab_widget = QTabWidget()
    axes = {}
    canvases = {}

    for name in graph_names:
        fig = Figure(figsize=(8.5, 5))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        tab_widget.addTab(canvas, name)
        axes[name] = ax
        canvases[name] = canvas

    return tab_widget, axes, canvases
