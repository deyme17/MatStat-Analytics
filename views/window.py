from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout,
    QSpinBox, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QDoubleSpinBox, QComboBox, QGroupBox, QMessageBox, QCheckBox
)
from PyQt6.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from models.data_model import Data
from models.data_processor import DataProcessor
from controllers.data_loader import load_data_file
from views.plot_graphs import plot_graphs
from controllers.dataUI_controller import DataUIController
from controllers.anomaly_controller import AnomalyController

class Window(QMainWindow):
    """Main window for statistical data analysis application."""
    def __init__(self, data_model, data_processor):
        super().__init__()
        self.setWindowTitle('MatStat')
        self.setWindowIcon(QIcon("resources/MatStat.jpeg"))
        self.resize(1200, 600) 

        # import some models
        self.data_model = data_model
        self.data_processor = data_processor

        self.ui_controller = DataUIController(self)
        self.data = None

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        """Create all UI widgets"""
        # buttons
        self.load_data_button = QPushButton('Load Data')
        self.load_data_button.setFixedSize(80, 25)
        self.load_data_button.clicked.connect(lambda: load_data_file(self))

        # bins
        self.bins_label = QLabel('Classes:')
        self.bins_label.setFixedWidth(60)  
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(1, 100)
        self.bins_spinbox.setValue(10)
        self.bins_spinbox.setEnabled(False)
        self.bins_spinbox.setFixedWidth(80)
        self.bins_spinbox.valueChanged.connect(lambda: plot_graphs(self))  

        # precision
        self.precision_label = QLabel('Precision:')
        self.precision_spinbox = QSpinBox()
        self.precision_spinbox.setRange(1, 6) 
        self.precision_spinbox.setValue(2)
        self.precision_spinbox.valueChanged.connect(lambda: plot_graphs(self))  
        
        # confidence level
        self.confidence_label = QLabel('Confidence level (for CI):')
        self.confidence_spinbox = QDoubleSpinBox()
        self.confidence_spinbox.setRange(0.80, 0.99)
        self.confidence_spinbox.setSingleStep(0.01)
        self.confidence_spinbox.setValue(0.95)
        self.confidence_spinbox.setDecimals(2)
        self.confidence_spinbox.valueChanged.connect(lambda: plot_graphs(self))

        # distribution checkboxes
        self.normal_dist_checkbox = QCheckBox("Normal Distribution")
        self.normal_dist_checkbox.stateChanged.connect(lambda: plot_graphs(self))
        
        self.exponential_dist_checkbox = QCheckBox("Exponential Distribution")
        self.exponential_dist_checkbox.stateChanged.connect(lambda: plot_graphs(self))

        # left panel tabs
        self.left_tab_widget = QTabWidget()
        
        # tab 1: Data Processing
        self.data_processing_widget = QWidget()
        self._create_data_processing_tab()
        self.left_tab_widget.addTab(self.data_processing_widget, "Data Processing")
        
        # tab 2: Statistic
        self.char_table = QTableWidget()
        self.char_table.setColumnCount(3)
        self.char_table.setHorizontalHeaderLabels(['Value', 'Lower CI', 'Upper CI'])
        self.char_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.left_tab_widget.addTab(self.char_table, "Statistic")
        
        # graph tabs
        self.graph_tab_widget = QTabWidget()
        
        # hist tab
        self.hist_figure = Figure(figsize=(8.5, 5))
        self.hist_canvas = FigureCanvas(self.hist_figure)
        self.hist_ax = self.hist_figure.add_subplot(111)
        self.graph_tab_widget.addTab(self.hist_canvas, "Histogram")
        
        # EDF tab
        self.edf_figure = Figure(figsize=(8.5, 5))
        self.edf_canvas = FigureCanvas(self.edf_figure)
        self.edf_ax = self.edf_figure.add_subplot(111)
        self.graph_tab_widget.addTab(self.edf_canvas, "Empirical Distribution Function")

    def _create_data_processing_tab(self):
        """Create Data Processing tab content"""
        layout = QVBoxLayout()
        
        # data version selection
        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        self.data_version_combo.currentIndexChanged.connect(
            self.ui_controller.on_data_version_changed
        )
        
        # transformation status label
        self.transformation_label = QLabel("Current state: Original")
        
        # data processing
        process_group = QGroupBox("Process Data")
        process_layout = QVBoxLayout()
        
        # standardize data
        self.standardize_button = QPushButton("Standardize")
        self.standardize_button.setEnabled(False)
        self.standardize_button.clicked.connect(self.ui_controller.standardize_data)
        self.standardize_button.setMinimumHeight(30)  
        
        # log transform
        self.log_button = QPushButton("Log Transform")
        self.log_button.setEnabled(False)
        self.log_button.clicked.connect(self.ui_controller.log_transform_data)
        self.log_button.setMinimumHeight(30)
        
        # shift data
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
        
        # anomaly detection group
        anomaly_group = QGroupBox("Anomaly Detection")
        anomaly_layout = QVBoxLayout()
        
        # create anomaly controller
        self.anomaly_controller = AnomalyController(self)
        
        # normal distribution anomaly detection
        self.normal_anomaly_button = QPushButton("Remove Anomalies (Normal)")
        self.normal_anomaly_button.setEnabled(False)
        self.normal_anomaly_button.clicked.connect(self.anomaly_controller.remove_normal_anomalies)
        self.normal_anomaly_button.setMinimumHeight(30)
        
        # simple anomaly detection
        self.asymmetry_anomaly_button = QPushButton("Remove Anomalies")
        self.asymmetry_anomaly_button.setEnabled(False)
        self.asymmetry_anomaly_button.clicked.connect(self.anomaly_controller.remove_anomalies)
        self.asymmetry_anomaly_button.setMinimumHeight(30)
        
        anomaly_layout.addWidget(self.normal_anomaly_button)
        anomaly_layout.addWidget(self.asymmetry_anomaly_button)
        anomaly_group.setLayout(anomaly_layout)
        
        # navigate
        nav_layout = QHBoxLayout()
        
        self.original_button = QPushButton("Original")
        self.original_button.setEnabled(False)
        self.original_button.clicked.connect(self.ui_controller.original_data)
        self.original_button.setMinimumHeight(30)
        
        nav_layout.addWidget(self.original_button)
        
        # proc layout
        process_layout.addWidget(self.standardize_button)
        process_layout.addWidget(self.log_button)
        process_layout.addLayout(shift_layout)
        process_group.setLayout(process_layout)
        
        # others layout
        layout.addWidget(self.data_version_label)
        layout.addWidget(self.data_version_combo)
        layout.addWidget(self.transformation_label)
        layout.addWidget(process_group)
        layout.addWidget(anomaly_group)
        layout.addLayout(nav_layout)
        layout.addStretch()
        
        self.data_processing_widget.setLayout(layout)

    def _create_layout(self):
        """Create the main window layout"""
    
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.load_data_button)

        controls_layout.addStretch()
        controls_layout.addWidget(self.confidence_label)
        controls_layout.addWidget(self.confidence_spinbox)
        controls_layout.addWidget(self.precision_label)
        controls_layout.addWidget(self.precision_spinbox)
        
        # graph horizontal layout
        bins_layout = QHBoxLayout()
        bins_layout.addWidget(self.bins_label)
        bins_layout.addWidget(self.bins_spinbox)
        bins_layout.addStretch()
        
        # distribution checkboxes layout
        dist_layout = QHBoxLayout()
        dist_layout.addWidget(self.normal_dist_checkbox)
        dist_layout.addWidget(self.exponential_dist_checkbox)
        dist_layout.addStretch()
        
        # graph panel
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.graph_tab_widget, stretch=1)
        right_panel.addLayout(bins_layout)
        right_panel.addLayout(dist_layout)
        
        # main layout
        main_panel = QHBoxLayout()
        main_panel.addWidget(self.left_tab_widget, stretch=1)
        main_panel.addLayout(right_panel, stretch=3)
        
        # final layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(main_panel, stretch=1)
        
        # central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def show_error_message(self, title, message):
        """Display error message dialog."""
        QMessageBox.critical(self, title, message)
        
    def show_info_message(self, title, message):
        """Display information message dialog."""
        QMessageBox.information(self, title, message)