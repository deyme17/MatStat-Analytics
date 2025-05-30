from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox
from utils.ui_styles import groupStyle

class AnomalyWidget(QGroupBox):
    """
    Widget for anomaly detection operations. 
    """

    def __init__(self, window):
        super().__init__("Anomaly Detection")
        self.setStyleSheet(groupStyle)
        layout = QVBoxLayout()

        # Button for removing normal (3σ) anomalies
        window.normal_anomaly_button = QPushButton("Remove 3σ anomalies")
        window.normal_anomaly_button.setEnabled(False)
        window.normal_anomaly_button.clicked.connect(window.anomaly_controller.remove_normal_anomalies)

        # Button for removing asymmetry-based anomalies
        window.asymmetry_anomaly_button = QPushButton("Remove assymetry anomalies")
        window.asymmetry_anomaly_button.setEnabled(False)
        window.asymmetry_anomaly_button.clicked.connect(window.anomaly_controller.remove_asymmetry_anomalies)

        # Button for removing anomalies based on confidence level gamma
        window.confidence_anomaly_button = QPushButton("Remove Anomalies by γ")
        window.confidence_anomaly_button.setEnabled(False)
        window.confidence_anomaly_button.clicked.connect(
            window.anomaly_controller.remove_conf_anomalies
        )

        # Controls for specifying the gamma level
        gamma_layout = QHBoxLayout()
        window.anomaly_gamma_label = QLabel("Significance level (1-γ):")
        window.anomaly_gamma_spinbox = QDoubleSpinBox()
        window.anomaly_gamma_spinbox.setRange(0.80, 0.99)
        window.anomaly_gamma_spinbox.setSingleStep(0.01)
        window.anomaly_gamma_spinbox.setValue(0.95)
        window.anomaly_gamma_spinbox.setDecimals(2)
        window.anomaly_gamma_spinbox.setEnabled(False)

        gamma_layout.addWidget(window.anomaly_gamma_label)
        gamma_layout.addWidget(window.anomaly_gamma_spinbox)

        # Assemble layout
        layout.addWidget(window.normal_anomaly_button)
        layout.addWidget(window.asymmetry_anomaly_button)
        layout.addWidget(window.confidence_anomaly_button)
        layout.addLayout(gamma_layout)
        self.setLayout(layout)
