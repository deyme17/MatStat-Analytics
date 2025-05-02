from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox
from utils.ui_styles import groupStyle

class ProcessDataWidget(QGroupBox):
    def __init__(self, window):
        super().__init__("Process Data")
        self.setStyleSheet(groupStyle)
        layout = QVBoxLayout()

        window.standardize_button = QPushButton("Standardize")
        window.standardize_button.setEnabled(False)
        window.standardize_button.clicked.connect(window.ui_controller.standardize_data)

        window.log_button = QPushButton("Log Transform")
        window.log_button.setEnabled(False)
        window.log_button.clicked.connect(window.ui_controller.log_transform_data)

        shift_layout = QHBoxLayout()
        window.shift_label = QLabel("Shift by:")
        window.shift_spinbox = QDoubleSpinBox()
        window.shift_spinbox.setRange(-1000, 1000)
        window.shift_spinbox.setSingleStep(1)
        window.shift_spinbox.setValue(0)
        window.shift_spinbox.setEnabled(False)
        window.shift_button = QPushButton("Apply")
        window.shift_button.setEnabled(False)
        window.shift_button.clicked.connect(window.ui_controller.shift_data)

        shift_layout.addWidget(window.shift_label)
        shift_layout.addWidget(window.shift_spinbox)
        shift_layout.addWidget(window.shift_button)

        layout.addWidget(window.standardize_button)
        layout.addWidget(window.log_button)
        layout.addLayout(shift_layout)
        self.setLayout(layout)