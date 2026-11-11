from PyQt6.QtWidgets import QHBoxLayout, QLabel
from controllers import AnomalyController
from utils import EventBus, EventType
from views.widgets.utils import make_alpha_spinbox
from .base import BaseDataWidget

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
             lambda: controller.remove_conf_anomalies(self.anomaly_gamma_spinbox.value()))
        ]
        super().__init__("Anomaly Detection", controller, event_bus, buttons_config)
        self._setup_gamma_controls()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        """Subscribe to missing values handling events."""
        self.event_bus.subscribe(EventType.MISSING_VALUES_DETECTED, self._disable_widget)
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._enable_widget)

    def _setup_gamma_controls(self) -> None:
        """Setup confidence level (gamma) controls."""
        gamma_layout = QHBoxLayout()
        
        self.anomaly_gamma_label = QLabel("Significance level (1-γ):")
        self.anomaly_gamma_spinbox = make_alpha_spinbox(
            min_val=MIN_GAMMA,
            max_val=MAX_GAMMA,
            step=GAMMA_STEP,
            decimals=GAMMA_PRECISION,
            default=DEFAULT_GAMMA
        )
        self.anomaly_gamma_spinbox.setEnabled(True)
        
        gamma_layout.addWidget(self.anomaly_gamma_label)
        gamma_layout.addWidget(self.anomaly_gamma_spinbox)
        
        self.add_layout(gamma_layout)