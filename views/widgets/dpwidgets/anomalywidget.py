from .base_dp_widget import BaseDataWidget
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox

MIN_GAMMA, MAX_GAMMA = 0.80, 0.99
GAMMA_STEP = 0.01
DEFAULT_GAMMA = 0.95
GAMMA_PRECISION = 2


class AnomalyWidget(BaseDataWidget):
    """Widget for anomaly detection operations."""
    def __init__(self, window):
        super().__init__("Anomaly Detection", window)
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components."""
        # Create buttons
        buttons_config = [
            ("sigma_anomaly_button", "Remove 3σ anomalies", 
             self.window.anomaly_controller.remove_sigma_anomalies),
            ("asymmetry_anomaly_button", "Remove asymmetry anomalies", 
             self.window.anomaly_controller.remove_asymmetry_anomalies),
            ("confidence_anomaly_button", "Remove Anomalies by γ", 
             self.window.anomaly_controller.remove_conf_anomalies)
        ]
        
        for attr_name, text, callback in buttons_config:
            button = QPushButton(text)
            button.setEnabled(False)
            button.clicked.connect(callback)
            setattr(self.window, attr_name, button)
            self.add_widget(button)
        
        # Gamma controls
        self._setup_gamma_controls()
    
    def _setup_gamma_controls(self):
        """Setup gamma level controls."""
        gamma_layout = QHBoxLayout()
        
        self.window.anomaly_gamma_label = QLabel("Significance level (1-γ):")
        self.window.anomaly_gamma_spinbox = QDoubleSpinBox()
        self.window.anomaly_gamma_spinbox.setRange(MIN_GAMMA, MAX_GAMMA)
        self.window.anomaly_gamma_spinbox.setSingleStep(GAMMA_STEP)
        self.window.anomaly_gamma_spinbox.setValue(DEFAULT_GAMMA)
        self.window.anomaly_gamma_spinbox.setDecimals(GAMMA_PRECISION)
        self.window.anomaly_gamma_spinbox.setEnabled(False)
        
        gamma_layout.addWidget(self.window.anomaly_gamma_label)
        gamma_layout.addWidget(self.window.anomaly_gamma_spinbox)
        
        self.add_layout(gamma_layout)