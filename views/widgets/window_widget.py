from PyQt6.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSpinBox, QDoubleSpinBox, QCheckBox, QGroupBox, QTableWidget, QHeaderView
)
from views.widgets.graphs_widget import DistributionWidget, create_test_group, create_graph_widgets
from utils.ui_styles import buttonStyle

class WindowWidgets:
    def __init__(self, window):
        self.window = window

    def create_controls_bar(self):
        self.window.load_data_button = QPushButton('Load Data')
        self.window.load_data_button.setFixedSize(80, 25)
        self.window.load_data_button.setStyleSheet(buttonStyle)

        self.window.confidence_label = QLabel('Confidence level (for CI):')
        self.window.confidence_spinbox = QDoubleSpinBox()
        self.window.confidence_spinbox.setRange(0.80, 0.99)
        self.window.confidence_spinbox.setSingleStep(0.01)
        self.window.confidence_spinbox.setValue(0.95)
        self.window.confidence_spinbox.setDecimals(2)

        self.window.precision_label = QLabel('Precision:')
        self.window.precision_spinbox = QSpinBox()
        self.window.precision_spinbox.setRange(1, 6)
        self.window.precision_spinbox.setValue(2)

        layout = QHBoxLayout()
        layout.addWidget(self.window.load_data_button)
        layout.addStretch()
        layout.addWidget(self.window.confidence_label)
        layout.addWidget(self.window.confidence_spinbox)
        layout.addWidget(self.window.precision_label)
        layout.addWidget(self.window.precision_spinbox)
        return layout

    def create_bins_layout(self):
        self.window.bins_label = QLabel('Classes:')
        self.window.bins_spinbox = QSpinBox()
        self.window.bins_spinbox.setRange(1, 100)
        self.window.bins_spinbox.setValue(10)
        self.window.bins_spinbox.setEnabled(False)

        self.window.show_smooth_edf_checkbox = QCheckBox("Show EDF curve with CI")
        self.window.show_smooth_edf_checkbox.setChecked(False)

        layout = QHBoxLayout()
        layout.addWidget(self.window.bins_label)
        layout.addWidget(self.window.bins_spinbox)
        layout.addSpacing(70)
        layout.addWidget(self.window.show_smooth_edf_checkbox)
        layout.addStretch()
        return layout

    def create_distribution_panel(self):
        self.window.dist_group = DistributionWidget(on_change=self.window.graph_plotter.plot_all)
        self.window.gof_group, self.window.test_labels = create_test_group([
            "Pearson's χ² test", "Kolmogorov-Smirnov test"])

        self.window.chi2_value_label = self.window.test_labels["Pearson's χ² test"]
        self.window.ks_value_label = self.window.test_labels["Kolmogorov-Smirnov test"]

        layout = QHBoxLayout()
        layout.addWidget(self.window.dist_group, 1)
        layout.addWidget(self.window.gof_group, 1)
        return layout

    def create_graph_area(self):
        self.window.graph_tab_widget, self.window.graph_axes, self.window.graph_canvases = create_graph_widgets([
            "Histogram", "Empirical Distribution Function"])

        self.window.hist_ax = self.window.graph_axes["Histogram"]
        self.window.hist_canvas = self.window.graph_canvases["Histogram"]
        self.window.edf_ax = self.window.graph_axes["Empirical Distribution Function"]
        self.window.edf_canvas = self.window.graph_canvases["Empirical Distribution Function"]

        return self.window.graph_tab_widget

    def create_statistic_table(self):
        self.window.char_table = QTableWidget()
        self.window.char_table.setColumnCount(3)
        self.window.char_table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
        self.window.char_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return self.window.char_table
