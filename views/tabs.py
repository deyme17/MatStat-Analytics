from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTableWidget, QHeaderView

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QGroupBox, QHBoxLayout, QPushButton, QDoubleSpinBox
)

class DataProcessingTab(QWidget):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        layout = QVBoxLayout()

        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        self.data_version_combo.currentIndexChanged.connect(window.ui_controller.on_data_version_changed)

        self.transformation_label = QLabel("Current state: Original")

        layout.addWidget(self.data_version_label)
        layout.addWidget(self.data_version_combo)
        layout.addWidget(self.transformation_label)

        layout.addWidget(self._create_process_group())
        layout.addWidget(self._create_anomaly_group())
        layout.addWidget(self._create_missing_group())
        layout.addLayout(window._create_nav_layout())
        layout.addStretch()

        self.setLayout(layout)

        window.data_version_label = self.data_version_label
        window.data_version_combo = self.data_version_combo
        window.transformation_label = self.transformation_label

    def _create_process_group(self):
        group = QGroupBox("Process Data")
        layout = QHBoxLayout()

        self.window.standardize_button = QPushButton("Standardize")
        self.window.standardize_button.clicked.connect(self.window.ui_controller.standardize_data)
        self.window.standardize_button.setEnabled(False)

        self.window.log_button = QPushButton("Log")
        self.window.log_button.clicked.connect(self.window.ui_controller.log_transform_data)
        self.window.log_button.setEnabled(False)

        self.window.shift_spinbox = QDoubleSpinBox()
        self.window.shift_spinbox.setRange(-1000.0, 1000.0)
        self.window.shift_spinbox.setDecimals(2)
        self.window.shift_spinbox.setSingleStep(0.1)
        self.window.shift_spinbox.setEnabled(False)

        self.window.shift_button = QPushButton("Shift")
        self.window.shift_button.clicked.connect(self.window.ui_controller.shift_data)
        self.window.shift_button.setEnabled(False)

        layout.addWidget(self.window.standardize_button)
        layout.addWidget(self.window.log_button)
        layout.addWidget(self.window.shift_spinbox)
        layout.addWidget(self.window.shift_button)

        group.setLayout(layout)
        return group

    def _create_anomaly_group(self):
        group = QGroupBox("Anomaly Detection")
        layout = QHBoxLayout()

        self.window.normal_anomaly_button = QPushButton("Normal")
        self.window.normal_anomaly_button.clicked.connect(lambda: self.window.anomaly_controller.remove_normal_anomalies())
        self.window.normal_anomaly_button.setEnabled(False)

        self.window.asymmetry_anomaly_button = QPushButton("Asymmetry")
        self.window.asymmetry_anomaly_button.clicked.connect(lambda: self.window.anomaly_controller.remove_anomalies())
        self.window.asymmetry_anomaly_button.setEnabled(False)

        self.window.anomaly_gamma_spinbox = QDoubleSpinBox()
        self.window.anomaly_gamma_spinbox.setRange(0.80, 0.99)
        self.window.anomaly_gamma_spinbox.setSingleStep(0.01)
        self.window.anomaly_gamma_spinbox.setValue(0.95)
        self.window.anomaly_gamma_spinbox.setDecimals(2)
        self.window.anomaly_gamma_spinbox.setEnabled(False)

        self.window.confidence_anomaly_button = QPushButton("CI")
        self.window.confidence_anomaly_button.clicked.connect(lambda: self.window.anomaly_controller.remove_confidence_interval_anomalies())
        self.window.confidence_anomaly_button.setEnabled(False)

        layout.addWidget(self.window.normal_anomaly_button)
        layout.addWidget(self.window.asymmetry_anomaly_button)
        layout.addWidget(self.window.anomaly_gamma_spinbox)
        layout.addWidget(self.window.confidence_anomaly_button)

        group.setLayout(layout)
        return group

    def _create_missing_group(self):
        group = QGroupBox("Missing Data")
        layout = QHBoxLayout()

        self.window.impute_mean_button = QPushButton("Mean")
        self.window.impute_mean_button.clicked.connect(lambda: self.window.missing_controller.impute_with_mean())
        self.window.impute_mean_button.setEnabled(False)

        self.window.impute_median_button = QPushButton("Median")
        self.window.impute_median_button.clicked.connect(lambda: self.window.missing_controller.impute_with_median())
        self.window.impute_median_button.setEnabled(False)

        self.window.interpolate_linear_button = QPushButton("Interpolate")
        self.window.interpolate_linear_button.clicked.connect(lambda: self.window.missing_controller.interpolate_missing("linear"))
        self.window.interpolate_linear_button.setEnabled(False)

        self.window.drop_missing_button = QPushButton("Drop")
        self.window.drop_missing_button.clicked.connect(lambda: self.window.missing_controller.drop_missing_values())
        self.window.drop_missing_button.setEnabled(False)

        layout.addWidget(self.window.impute_mean_button)
        layout.addWidget(self.window.impute_median_button)
        layout.addWidget(self.window.interpolate_linear_button)
        layout.addWidget(self.window.drop_missing_button)

        group.setLayout(layout)
        return group


def create_statistic_tab():
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    return table