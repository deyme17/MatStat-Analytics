from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox
from controllers.anomaly_controller import AnomalyController
from utils.ui_styles import groupStyle

class AnomalyWidget(QGroupBox):
    def __init__(self, window):
        super().__init__("Anomaly Detection")
        self.setStyleSheet(groupStyle)
        layout = QVBoxLayout()

        window.anomaly_controller = AnomalyController(window)

        window.normal_anomaly_button = QPushButton("Remove Anomalies (3σ)")
        window.normal_anomaly_button.setEnabled(False)
        window.normal_anomaly_button.clicked.connect(window.anomaly_controller.remove_normal_anomalies)

        window.asymmetry_anomaly_button = QPushButton("Remove Anomalies (A)")
        window.asymmetry_anomaly_button.setEnabled(False)
        window.asymmetry_anomaly_button.clicked.connect(window.anomaly_controller.remove_anomalies)

        window.confidence_anomaly_button = QPushButton("Remove Anomalies (γ)")
        window.confidence_anomaly_button.setEnabled(False)
        window.confidence_anomaly_button.clicked.connect(
            window.anomaly_controller.remove_confidence_interval_anomalies
        )

        gamma_layout = QHBoxLayout()
        window.anomaly_gamma_label = QLabel("Data Confident level (1-γ):")
        window.anomaly_gamma_spinbox = QDoubleSpinBox()
        window.anomaly_gamma_spinbox.setRange(0.80, 0.99)
        window.anomaly_gamma_spinbox.setSingleStep(0.01)
        window.anomaly_gamma_spinbox.setValue(0.95)
        window.anomaly_gamma_spinbox.setDecimals(2)
        window.anomaly_gamma_spinbox.setEnabled(False)

        gamma_layout.addWidget(window.anomaly_gamma_label)
        gamma_layout.addWidget(window.anomaly_gamma_spinbox)

        layout.addWidget(window.normal_anomaly_button)
        layout.addWidget(window.asymmetry_anomaly_button)
        layout.addWidget(window.confidence_anomaly_button)
        layout.addLayout(gamma_layout)
        self.setLayout(layout)
