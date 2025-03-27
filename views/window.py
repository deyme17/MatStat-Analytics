from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout,
    QSpinBox, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QDoubleSpinBox, QComboBox, QGroupBox, QMessageBox, QCheckBox, QGridLayout
)
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys

from controllers.missing_controller import MissingDataController
from controllers.data_loader import load_data_file
from views.plot_graphs import plot_graphs
from controllers.dataUI_controller import DataUIController
from controllers.anomaly_controller import AnomalyController

class Window(QMainWindow):
    def __init__(self, data_model, data_processor):
        super().__init__()
        self.setWindowTitle('MatStat Analytics')
        self.setWindowIcon(QIcon("resources/MatStat.jpeg"))
        self.resize(1400, 800)

        # palette
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 248, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(245, 250, 255))
        self.setPalette(palette)

        self.data_model = data_model
        self.data_processor = data_processor
        self.ui_controller = DataUIController(self)
        self.data = None

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        self.load_data_button = QPushButton('Load Data')
        self.load_data_button.setFixedSize(80, 25)
        self.load_data_button.clicked.connect(lambda: load_data_file(self))

        self.bins_label = QLabel('Classes:')
        self.bins_label.setFixedWidth(60)  
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(1, 100)
        self.bins_spinbox.setValue(10)
        self.bins_spinbox.setEnabled(False)
        self.bins_spinbox.setFixedWidth(80)
        self.bins_spinbox.valueChanged.connect(lambda: plot_graphs(self))  

        self.precision_label = QLabel('Precision:')
        self.precision_spinbox = QSpinBox()
        self.precision_spinbox.setRange(1, 6) 
        self.precision_spinbox.setValue(2)
        self.precision_spinbox.valueChanged.connect(lambda: plot_graphs(self))  
        
        self.confidence_label = QLabel('Confidence level (for CI):')
        self.confidence_spinbox = QDoubleSpinBox()
        self.confidence_spinbox.setRange(0.80, 0.99)
        self.confidence_spinbox.setSingleStep(0.01)
        self.confidence_spinbox.setValue(0.95)
        self.confidence_spinbox.setDecimals(2)
        self.confidence_spinbox.valueChanged.connect(lambda: plot_graphs(self))

        self.dist_group = QGroupBox("Statistical Distributions")
        dist_layout = QVBoxLayout()
        
        dist_row = QHBoxLayout()
        self.normal_dist_checkbox = QCheckBox("Normal")
        self.normal_dist_checkbox.stateChanged.connect(lambda: plot_graphs(self))
        dist_row.addWidget(self.normal_dist_checkbox)
        
        self.exponential_dist_checkbox = QCheckBox("Exponential")
        self.exponential_dist_checkbox.stateChanged.connect(lambda: plot_graphs(self))
        dist_row.addWidget(self.exponential_dist_checkbox)
        
        self.uniform_dist_checkbox = QCheckBox("Uniform")
        self.uniform_dist_checkbox.stateChanged.connect(lambda: plot_graphs(self))
        dist_row.addWidget(self.uniform_dist_checkbox)
        
        self.weibull_dist_checkbox = QCheckBox("Weibull")
        self.weibull_dist_checkbox.stateChanged.connect(lambda: plot_graphs(self))
        dist_row.addWidget(self.weibull_dist_checkbox)
        
        # EDF options
        edf_options_row = QHBoxLayout()
        self.show_smooth_edf_checkbox = QCheckBox("Show Smooth EDF with CI")
        self.show_smooth_edf_checkbox.setChecked(True)
        self.show_smooth_edf_checkbox.stateChanged.connect(lambda: plot_graphs(self))
        edf_options_row.addWidget(self.show_smooth_edf_checkbox)
        edf_options_row.addStretch()
        
        dist_layout.addLayout(dist_row)
        dist_layout.addLayout(edf_options_row)
        self.dist_group.setLayout(dist_layout)

        # button styles
        button_style = """
        QPushButton {
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:disabled {
            background-color: #bdc3c7;
        }
        """
        self.load_data_button.setStyleSheet(button_style)

        self.left_tab_widget = QTabWidget()
        
        self.data_processing_widget = QWidget()
        self._create_data_processing_tab()
        self.left_tab_widget.addTab(self.data_processing_widget, "Data Processing")
        
        self.char_table = QTableWidget()
        self.char_table.setColumnCount(3)
        self.char_table.setHorizontalHeaderLabels(['Value', 'Lower CI', 'Upper CI'])
        self.char_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.left_tab_widget.addTab(self.char_table, "Statistic")
        
        self.graph_tab_widget = QTabWidget()
        
        self.hist_figure = Figure(figsize=(8.5, 5))
        self.hist_canvas = FigureCanvas(self.hist_figure)
        self.hist_ax = self.hist_figure.add_subplot(111)
        self.graph_tab_widget.addTab(self.hist_canvas, "Histogram")
        
        self.edf_figure = Figure(figsize=(8.5, 5))
        self.edf_canvas = FigureCanvas(self.edf_figure)
        self.edf_ax = self.edf_figure.add_subplot(111)
        self.graph_tab_widget.addTab(self.edf_canvas, "Empirical Distribution Function")

    def _create_data_processing_tab(self):
        layout = QVBoxLayout()
        
        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        self.data_version_combo.currentIndexChanged.connect(
            self.ui_controller.on_data_version_changed
        )
        
        self.transformation_label = QLabel("Current state: Original")
        
        # process Data group
        process_group = QGroupBox("Process Data")
        process_layout = QVBoxLayout()
        
        self.standardize_button = QPushButton("Standardize")
        self.standardize_button.setEnabled(False)
        self.standardize_button.clicked.connect(self.ui_controller.standardize_data)
        self.standardize_button.setMinimumHeight(30)  
        
        self.log_button = QPushButton("Log Transform")
        self.log_button.setEnabled(False)
        self.log_button.clicked.connect(self.ui_controller.log_transform_data)
        self.log_button.setMinimumHeight(30)
        
        shift_layout = QHBoxLayout()
        self.shift_label = QLabel("Shift by:")
        self.shift_spinbox = QDoubleSpinBox()
        self.shift_spinbox.setRange(-1000, 1000)
        self.shift_spinbox.setSingleStep(1)
        self.shift_spinbox.setValue(0)
        self.shift_spinbox.setEnabled(False)
        self.shift_button = QPushButton("Apply")
        self.shift_button.setEnabled(False)
        self.shift_button.clicked.connect(self.ui_controller.shift_data)
        self.shift_button.setMinimumHeight(30) 
        shift_layout.addWidget(self.shift_label)
        shift_layout.addWidget(self.shift_spinbox)
        shift_layout.addWidget(self.shift_button)
        
        # anomaly group
        anomaly_group = QGroupBox("Anomaly Detection")
        anomaly_layout = QVBoxLayout()
        
        self.anomaly_controller = AnomalyController(self)
        
        self.normal_anomaly_button = QPushButton("Remove Anomalies (Normal)")
        self.normal_anomaly_button.setEnabled(False)
        self.normal_anomaly_button.clicked.connect(self.anomaly_controller.remove_normal_anomalies)
        self.normal_anomaly_button.setMinimumHeight(30)
        
        self.asymmetry_anomaly_button = QPushButton("Remove Anomalies")
        self.asymmetry_anomaly_button.setEnabled(False)
        self.asymmetry_anomaly_button.clicked.connect(self.anomaly_controller.remove_anomalies)
        self.asymmetry_anomaly_button.setMinimumHeight(30)
        
        anomaly_layout.addWidget(self.normal_anomaly_button)
        anomaly_layout.addWidget(self.asymmetry_anomaly_button)
        anomaly_group.setLayout(anomaly_layout)
        
        # missings group
        missing_group = QGroupBox("Missing Data")
        missing_layout = QVBoxLayout()
        
        self.missing_controller = MissingDataController(self)
        
        # info labels about missing data
        missing_info_layout = QVBoxLayout()
        self.missing_count_label = QLabel("Total Missing: 0")
        self.missing_percentage_label = QLabel("Missing Percentage: 0.00%")
        missing_info_layout.addWidget(self.missing_count_label)
        missing_info_layout.addWidget(self.missing_percentage_label)
        
        # buttons for handling missing data
        self.impute_mean_button = QPushButton("Replace with Mean")
        self.impute_mean_button.setEnabled(False)
        self.impute_mean_button.clicked.connect(self.missing_controller.impute_with_mean)
        self.impute_mean_button.setMinimumHeight(30)
        
        self.impute_median_button = QPushButton("Replace with Median")
        self.impute_median_button.setEnabled(False)
        self.impute_median_button.clicked.connect(self.missing_controller.impute_with_median)
        self.impute_median_button.setMinimumHeight(30)
        
        self.interpolate_linear_button = QPushButton("Interpolate (Linear)")
        self.interpolate_linear_button.setEnabled(False)
        self.interpolate_linear_button.clicked.connect(lambda: self.missing_controller.interpolate_missing("linear"))
        self.interpolate_linear_button.setMinimumHeight(30)
        
        self.drop_missing_button = QPushButton("Drop Missing Values")
        self.drop_missing_button.setEnabled(False)
        self.drop_missing_button.clicked.connect(self.missing_controller.drop_missing_values)
        self.drop_missing_button.setMinimumHeight(30)
        
        missing_layout.addLayout(missing_info_layout)
        missing_layout.addWidget(self.impute_mean_button)
        missing_layout.addWidget(self.impute_median_button)
        missing_layout.addWidget(self.interpolate_linear_button)
        missing_layout.addWidget(self.drop_missing_button)
        missing_group.setLayout(missing_layout)
        
        # navig
        nav_layout = QHBoxLayout()
        
        self.original_button = QPushButton("Original")
        self.original_button.setEnabled(False)
        self.original_button.clicked.connect(self.ui_controller.original_data)
        self.original_button.setMinimumHeight(30)
        
        nav_layout.addWidget(self.original_button)
        
        # elements to the process layout
        process_layout.addWidget(self.standardize_button)
        process_layout.addWidget(self.log_button)
        process_layout.addLayout(shift_layout)
        process_group.setLayout(process_layout)
        
        # stylesheet to group
        group_style = """
        QGroupBox {
            border: 2px solid #87ceeb;
            border-radius: 10px;
            margin-top: 10px;
            background-color: rgba(135, 206, 235, 0.1);
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
        }
        """
        process_group.setStyleSheet(group_style)
        anomaly_group.setStyleSheet(group_style)
        missing_group.setStyleSheet(group_style)
        
        # ddd all elements to the main layout
        layout.addWidget(self.data_version_label)
        layout.addWidget(self.data_version_combo)
        layout.addWidget(self.transformation_label)
        layout.addWidget(process_group)
        layout.addWidget(anomaly_group)
        layout.addWidget(missing_group)
        layout.addLayout(nav_layout)
        layout.addStretch()
        
        self.data_processing_widget.setLayout(layout)

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
        bins_layout.addStretch()
        
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.graph_tab_widget, stretch=1)
        right_panel.addLayout(bins_layout)
        
        # add the dist group
        right_panel.addWidget(self.dist_group)
        
        main_panel = QHBoxLayout()
        main_panel.addWidget(self.left_tab_widget, stretch=1)
        main_panel.addLayout(right_panel, stretch=3)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(main_panel, stretch=1)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def show_error_message(self, title, message):
        QMessageBox.critical(self, title, message)
        
    def show_info_message(self, title, message):
        QMessageBox.information(self, title, message)