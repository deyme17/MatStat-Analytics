from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout,
    QSpinBox, QLabel, QTableWidget, QHeaderView, QTabWidget,
    QDoubleSpinBox, QMessageBox, QCheckBox
)
from PyQt6.QtGui import QIcon, QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from controllers.data_loader import load_data_file
from controllers.dataUI_controller import DataUIController
from controllers.anomaly_controller import AnomalyController
from controllers.missing_controller import MissingDataController

from views.data_processing_tab import DataProcessingTab
from views.widgets import DistributionWidget, create_test_group, create_graph_widgets
from views.graph_plotter import GraphPlotter
from utils.ui_styles import appStyle, buttonStyle

class Window(QMainWindow):
    def __init__(self, data_model, data_processor):
        super().__init__()
        self.setWindowTitle('MatStat Analytics')
        self.setWindowIcon(QIcon("resources/MatStat.jpeg"))
        self.resize(1400, 800)

        self._init_palette()
        self.setStyleSheet(appStyle)

        self.data_model = data_model
        self.data_processor = data_processor
        self.ui_controller = DataUIController(self)
        self.anomaly_controller = AnomalyController(self)
        self.missing_controller = MissingDataController(self)
        self.data = None

        self._create_widgets()
        self._create_layout()

    def _init_palette(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 248, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(245, 250, 255))
        self.setPalette(palette)

    def _create_widgets(self):
        self.load_data_button = QPushButton('Load Data')
        self.load_data_button.setFixedSize(80, 25)
        self.load_data_button.setStyleSheet(buttonStyle)
        self.load_data_button.clicked.connect(lambda: load_data_file(self))

        self.bins_label = QLabel('Classes:')
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(1, 100)
        self.bins_spinbox.setValue(10)
        self.bins_spinbox.setEnabled(False)
        self.bins_spinbox.valueChanged.connect(lambda: GraphPlotter(self).plot_all())

        self.show_smooth_edf_checkbox = QCheckBox("Show EDF curve with CI")
        self.show_smooth_edf_checkbox.setChecked(False)
        self.show_smooth_edf_checkbox.stateChanged.connect(lambda: GraphPlotter(self).plot_all())

        self.precision_label = QLabel('Precision:')
        self.precision_spinbox = QSpinBox()
        self.precision_spinbox.setRange(1, 6)
        self.precision_spinbox.setValue(2)
        self.precision_spinbox.valueChanged.connect(lambda: GraphPlotter(self).plot_all())

        self.confidence_label = QLabel('Confidence level (for CI):')
        self.confidence_spinbox = QDoubleSpinBox()
        self.confidence_spinbox.setRange(0.80, 0.99)
        self.confidence_spinbox.setSingleStep(0.01)
        self.confidence_spinbox.setValue(0.95)
        self.confidence_spinbox.setDecimals(2)
        self.confidence_spinbox.valueChanged.connect(lambda: GraphPlotter(self).plot_all())

        self.dist_group = DistributionWidget(on_change=lambda: GraphPlotter(self).plot_all())
        self.gof_group, self.test_labels = create_test_group(["Pearson's χ² test", "Kolmogorov-Smirnov test"])
        self.chi2_value_label = self.test_labels["Pearson's χ² test"]
        self.ks_value_label = self.test_labels["Kolmogorov-Smirnov test"]

        self.graph_tab_widget, self.graph_axes, self.graph_canvases = create_graph_widgets(["Histogram", "Empirical Distribution Function"])
        self.hist_ax = self.graph_axes["Histogram"]
        self.hist_canvas = self.graph_canvases["Histogram"]
        self.edf_ax = self.graph_axes["Empirical Distribution Function"]
        self.edf_canvas = self.graph_canvases["Empirical Distribution Function"]

        self.char_table = QTableWidget()
        self.char_table.setColumnCount(3)
        self.char_table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
        self.char_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.left_tab_widget = QTabWidget()
        self.left_tab_widget.addTab(DataProcessingTab(self), "Data Processing")
        self.left_tab_widget.addTab(self.char_table, "Statistic")

    def _create_layout(self):
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.load_data_button)
        controls_layout.addStretch()
        controls_layout.addWidget(self.confidence_label)
        controls_layout.addWidget(self.confidence_spinbox)
        controls_layout.addWidget(self.precision_label)
        controls_layout.addWidget(self.precision_spinbox)

        bins_layout = QHBoxLayout()
        bins_layout.addWidget(self.bins_label)
        bins_layout.addWidget(self.bins_spinbox)
        bins_layout.addSpacing(70)
        bins_layout.addWidget(self.show_smooth_edf_checkbox)
        bins_layout.addStretch()

        dist_gof_layout = QHBoxLayout()
        dist_gof_layout.addWidget(self.dist_group, 1)
        dist_gof_layout.addWidget(self.gof_group, 1)

        right_panel = QVBoxLayout()
        right_panel.addWidget(self.graph_tab_widget, stretch=1)
        right_panel.addLayout(bins_layout)
        right_panel.addLayout(dist_gof_layout)

        main_panel = QHBoxLayout()
        main_panel.addWidget(self.left_tab_widget, stretch=1)
        main_panel.addLayout(right_panel, stretch=3)

        main_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(main_panel, stretch=1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _create_nav_layout(self):
        nav_layout = QHBoxLayout()
        self.original_button = QPushButton("Original")
        self.original_button.setEnabled(False)
        self.original_button.clicked.connect(self.ui_controller.original_data)
        self.original_button.setMinimumHeight(30)
        nav_layout.addWidget(self.original_button)
        return nav_layout

    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)

    def show_info_message(self, title, message):
        QMessageBox.information(self, title, message)
