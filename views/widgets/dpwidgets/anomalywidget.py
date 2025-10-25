from .base_dp_widget import BaseDataWidget
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QDoubleSpinBox
from controllers import AnomalyController
from utils import EventBus, EventType

MIN_GAMMA, MAX_GAMMA = 0.80, 0.99
GAMMA_STEP = 0.01
DEFAULT_GAMMA = 0.95
GAMMA_PRECISION = 2


class AnomalyWidget(BaseDataWidget):
    """Widget for anomaly detection operations."""
    def __init__(self, controller: AnomalyController, event_bus: EventBus):
        buttons_config = [
            ("sigma_anomaly_button", "Remove 3σ anomalies", 
             controller.remove_sigma_anomalies),
            ("asymmetry_anomaly_button", "Remove asymmetry anomalies", 
             controller.remove_asymmetry_anomalies),
            ("confidence_anomaly_button", "Remove Anomalies by γ", 
             controller.remove_conf_anomalies)
        ]
        super().__init__("Anomaly Detection", controller, event_bus, buttons_config)
        # gamma controls
        self._setup_gamma_controls()
        # subscibe to events
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.MISSING_VALUES_DETECTED, self._disable_widget)
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._unable_widget)

    def _setup_gamma_controls(self):
        """Setup gamma level controls."""
        gamma_layout = QHBoxLayout()
        
        self.anomaly_gamma_label = QLabel("Significance level (1-γ):")
        self.anomaly_gamma_spinbox = QDoubleSpinBox()
        self.anomaly_gamma_spinbox.setRange(MIN_GAMMA, MAX_GAMMA)
        self.anomaly_gamma_spinbox.setSingleStep(GAMMA_STEP)
        self.anomaly_gamma_spinbox.setValue(DEFAULT_GAMMA)
        self.anomaly_gamma_spinbox.setDecimals(GAMMA_PRECISION)
        self.anomaly_gamma_spinbox.setEnabled(False)
        
        gamma_layout.addWidget(self.anomaly_gamma_label)
        gamma_layout.addWidget(self.anomaly_gamma_spinbox)
        
        self.add_layout(gamma_layout)