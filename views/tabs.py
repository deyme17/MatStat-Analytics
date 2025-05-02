from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTableWidget, QHeaderView

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QGroupBox, QHBoxLayout, QPushButton, QDoubleSpinBox
)

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox, QComboBox
from controllers.anomaly_controller import AnomalyController
from controllers.missing_controller import MissingDataController
from utils.ui_styles import groupStyle

# 1
class DataProcessingTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        self.data_version_combo.currentIndexChanged.connect(parent.ui_controller.on_data_version_changed)

        self.transformation_label = QLabel("Current state: Original")

        self.process_controls = self._createDataProcessingWidget(parent)
        self.anomaly_detection = self._createAnomalyDetectionWidget(parent)
        self.missing_data = self._createMissingDataWidget(parent)

        layout = QVBoxLayout()
        layout.addWidget(self.data_version_label)
        layout.addWidget(self.data_version_combo)
        layout.addWidget(self.transformation_label)
        layout.addWidget(self.process_controls)
        layout.addWidget(self.anomaly_detection)
        layout.addWidget(self.missing_data)
        layout.addLayout(parent._create_nav_layout())
        layout.addStretch()

        self.setLayout(layout)

        parent.data_version_label = self.data_version_label
        parent.data_version_combo = self.data_version_combo
        parent.transformation_label = self.transformation_label

    def _createDataProcessingWidget(self, parent):
        group = QGroupBox("Process Data")
        group.setStyleSheet(groupStyle)
        layout = QVBoxLayout()

        parent.standardize_button = QPushButton("Standardize")
        parent.standardize_button.setEnabled(False)
        parent.standardize_button.clicked.connect(parent.ui_controller.standardize_data)

        parent.log_button = QPushButton("Log Transform")
        parent.log_button.setEnabled(False)
        parent.log_button.clicked.connect(parent.ui_controller.log_transform_data)

        shift_layout = QHBoxLayout()
        parent.shift_label = QLabel("Shift by:")
        parent.shift_spinbox = QDoubleSpinBox()
        parent.shift_spinbox.setRange(-1000, 1000)
        parent.shift_spinbox.setSingleStep(1)
        parent.shift_spinbox.setValue(0)
        parent.shift_spinbox.setEnabled(False)
        parent.shift_button = QPushButton("Apply")
        parent.shift_button.setEnabled(False)
        parent.shift_button.clicked.connect(parent.ui_controller.shift_data)

        shift_layout.addWidget(parent.shift_label)
        shift_layout.addWidget(parent.shift_spinbox)
        shift_layout.addWidget(parent.shift_button)

        layout.addWidget(parent.standardize_button)
        layout.addWidget(parent.log_button)
        layout.addLayout(shift_layout)
        group.setLayout(layout)
        return group

    def _createAnomalyDetectionWidget(self, parent):
        group = QGroupBox("Anomaly Detection")
        group.setStyleSheet(groupStyle)
        layout = QVBoxLayout()

        parent.anomaly_controller = AnomalyController(parent)

        parent.normal_anomaly_button = QPushButton("Remove Anomalies (3σ)")
        parent.normal_anomaly_button.setEnabled(False)
        parent.normal_anomaly_button.clicked.connect(parent.anomaly_controller.remove_normal_anomalies)

        parent.asymmetry_anomaly_button = QPushButton("Remove Anomalies (A)")
        parent.asymmetry_anomaly_button.setEnabled(False)
        parent.asymmetry_anomaly_button.clicked.connect(parent.anomaly_controller.remove_anomalies)

        parent.confidence_anomaly_button = QPushButton("Remove Anomalies (γ)")
        parent.confidence_anomaly_button.setEnabled(False)
        parent.confidence_anomaly_button.clicked.connect(
            parent.anomaly_controller.remove_confidence_interval_anomalies
        )

        gamma_layout = QHBoxLayout()
        parent.anomaly_gamma_label = QLabel("Data Confident level (1-γ):")
        parent.anomaly_gamma_spinbox = QDoubleSpinBox()
        parent.anomaly_gamma_spinbox.setRange(0.80, 0.99)
        parent.anomaly_gamma_spinbox.setSingleStep(0.01)
        parent.anomaly_gamma_spinbox.setValue(0.95)
        parent.anomaly_gamma_spinbox.setDecimals(2)
        parent.anomaly_gamma_spinbox.setEnabled(False)

        gamma_layout.addWidget(parent.anomaly_gamma_label)
        gamma_layout.addWidget(parent.anomaly_gamma_spinbox)

        layout.addWidget(parent.normal_anomaly_button)
        layout.addWidget(parent.asymmetry_anomaly_button)
        layout.addWidget(parent.confidence_anomaly_button)
        layout.addLayout(gamma_layout)

        group.setLayout(layout)
        return group

    def _createMissingDataWidget(self, parent):
        group = QGroupBox("Missing Data")
        group.setStyleSheet(groupStyle)
        layout = QVBoxLayout()

        parent.missing_controller = MissingDataController(parent)

        parent.missing_count_label = QLabel("Total Missing: 0")
        parent.missing_percentage_label = QLabel("Missing Percentage: 0.00%")

        parent.impute_mean_button = QPushButton("Replace with Mean")
        parent.impute_mean_button.setEnabled(False)
        parent.impute_mean_button.clicked.connect(parent.missing_controller.impute_with_mean)

        parent.impute_median_button = QPushButton("Replace with Median")
        parent.impute_median_button.setEnabled(False)
        parent.impute_median_button.clicked.connect(parent.missing_controller.impute_with_median)

        parent.interpolate_linear_button = QPushButton("Interpolate (Linear)")
        parent.interpolate_linear_button.setEnabled(False)
        parent.interpolate_linear_button.clicked.connect(
            lambda: parent.missing_controller.interpolate_missing("linear")
        )

        parent.drop_missing_button = QPushButton("Drop Missing Values")
        parent.drop_missing_button.setEnabled(False)
        parent.drop_missing_button.clicked.connect(parent.missing_controller.drop_missing_values)

        layout.addWidget(parent.missing_count_label)
        layout.addWidget(parent.missing_percentage_label)
        layout.addWidget(parent.impute_mean_button)
        layout.addWidget(parent.impute_median_button)
        layout.addWidget(parent.interpolate_linear_button)
        layout.addWidget(parent.drop_missing_button)

        group.setLayout(layout)
        return group

# 2
def create_statistic_tab():
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    return table