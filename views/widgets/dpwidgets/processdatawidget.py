from .base_dp_widget import BaseDataWidget
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox

MIN_SHIFT, MAX_SHIFT = -1000, 1000
SHIFT_STEP = 1
DEFAULT_SHIFT = 0


class ProcessDataWidget(BaseDataWidget):
    """Widget for performing basic data transformations."""
    
    def __init__(self, window):
        super().__init__("Process Data", window)
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components."""
        # Transformation buttons
        buttons_config = [
            ("standardize_button", "Standardize", 
             self.window.transform_controller.standardize_data),
            ("log_button", "Log Transform", 
             self.window.transform_controller.log_transform_data)
        ]
        
        for attr_name, text, callback in buttons_config:
            button = QPushButton(text)
            button.setEnabled(False)
            button.clicked.connect(callback)
            setattr(self.window, attr_name, button)
            self.add_widget(button)

        # Shift controls
        self._setup_shift_controls()
    
    def _setup_shift_controls(self):
        """Setup shift controls."""
        shift_layout = QHBoxLayout()
        
        self.window.shift_label = QLabel("Shift by:")
        self.window.shift_spinbox = QDoubleSpinBox()
        self.window.shift_spinbox.setRange(MIN_SHIFT, MAX_SHIFT)
        self.window.shift_spinbox.setSingleStep(SHIFT_STEP)
        self.window.shift_spinbox.setValue(DEFAULT_SHIFT)
        self.window.shift_spinbox.setEnabled(False)
        
        self.window.shift_button = QPushButton("Apply")
        self.window.shift_button.setEnabled(False)
        self.window.shift_button.clicked.connect(self.window.transform_controller.shift_data)
        
        shift_layout.addWidget(self.window.shift_label)
        shift_layout.addWidget(self.window.shift_spinbox)
        shift_layout.addWidget(self.window.shift_button)
        
        self.add_layout(shift_layout)