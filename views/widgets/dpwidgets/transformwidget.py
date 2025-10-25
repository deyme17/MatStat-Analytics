from .base_dp_widget import BaseDataWidget
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox
from controllers import DataTransformController
from utils import EventBus, EventType, Event

MIN_SHIFT, MAX_SHIFT = -1000, 1000
SHIFT_STEP = 1
DEFAULT_SHIFT = 0


class TransformDataWidget(BaseDataWidget):
    """Widget for performing basic data transformations."""
    def __init__(self, controller: DataTransformController, event_bus: EventBus):
        buttons_config = [
            ("standardize_button", "Standardize", 
             controller.standardize_data),
            ("log_button", "Log Transform", 
             controller.log_transform_data)
        ]
        super().__init__("Process Data", controller, event_bus, buttons_config)
        # shift controls
        self._setup_shift_controls()
        # subscribe to events
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.MISSING_VALUES_DETECTED, self._disable_widget)
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._unable_widget)
    
    def _setup_shift_controls(self):
        """Setup shift controls."""
        shift_layout = QHBoxLayout()
        
        self.shift_label = QLabel("Shift by:")
        self.shift_spinbox = QDoubleSpinBox()
        self.shift_spinbox.setRange(MIN_SHIFT, MAX_SHIFT)
        self.shift_spinbox.setSingleStep(SHIFT_STEP)
        self.shift_spinbox.setValue(DEFAULT_SHIFT)
        self.shift_spinbox.setEnabled(False)
        
        self.shift_button = QPushButton("Apply")
        self.shift_button.setEnabled(False)
        self.shift_button.clicked.connect(self.controller.shift_data)
        
        shift_layout.addWidget(self.shift_label)
        shift_layout.addWidget(self.shift_spinbox)
        shift_layout.addWidget(self.shift_button)
        
        self.add_layout(shift_layout)