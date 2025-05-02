from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox
from controllers.anomaly_controller import AnomalyController
from utils.ui_styles import groupStyle

class AnomalyWidget(QGroupBox):
    def __init__(self, parent):
        super().__init__("Anomaly Detection")
        self.setStyleSheet(groupStyle)
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
        self.setLayout(layout)
