from .base_dp_widget import BaseDataWidget
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox

MIN_SHIFT, MAX_SHIFT = -1000, 1000
SHIFT_STEP = 1
DEFAULT_SHIFT = 0

class TransformDataWidget(BaseDataWidget):
    """Widget for performing basic data transformations."""
    def __init__(self, controller):
        super().__init__("Process Data", controller)
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components."""
        # Transformation buttons
        buttons_config = [
            ("standardize_button", "Standardize", 
             self.controller.standardize_data),
            ("log_button", "Log Transform", 
             self.controller.log_transform_data)
        ]
        
        for attr_name, text, callback in buttons_config:
            button = QPushButton(text)
            button.setEnabled(False)
            button.clicked.connect(callback)
            setattr(self.attr, attr_name, button)
            self.add_widget(button)

        # Shift controls
        self._setup_shift_controls()
    
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