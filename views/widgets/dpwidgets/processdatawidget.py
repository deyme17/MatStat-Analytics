from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDoubleSpinBox
from utils.ui_styles import groupStyle

class ProcessDataWidget(QGroupBox):
    def __init__(self, parent):
        super().__init__("Process Data")
        self.setStyleSheet(groupStyle)
        layout = QVBoxLayout()

        parent.standardize_button = QPushButton("Standardize")
        parent.standardize_button.setEnabled(False)
        parent.standardize_button.clicked.connect(parent.ui_controller.standardize_data)

        parent.log_button = QPushButton("Log Transform")
        parent.log_button.setEnabled(False)
        parent.log_button.clicked.connect(parent.ui_controller.log_transform_data)

        shift_layout = QHBoxLayout()
        parent.shift_label = QLabel("Shift by:")
        parent.shift_spinbox = QDoubleSpinBox()
        parent.shift_spinbox.setRange(-1000, 1000)
        parent.shift_spinbox.setSingleStep(1)
        parent.shift_spinbox.setValue(0)
        parent.shift_spinbox.setEnabled(False)
        parent.shift_button = QPushButton("Apply")
        parent.shift_button.setEnabled(False)
        parent.shift_button.clicked.connect(parent.ui_controller.shift_data)

        shift_layout.addWidget(parent.shift_label)
        shift_layout.addWidget(parent.shift_spinbox)
        shift_layout.addWidget(parent.shift_button)

        layout.addWidget(parent.standardize_button)
        layout.addWidget(parent.log_button)
        layout.addLayout(shift_layout)
        self.setLayout(layout)