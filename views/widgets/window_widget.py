from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSpinBox, QDoubleSpinBox, QCheckBox

class WindowWidgets:
    def __init__(self, window):
        self.window = window

    def create_controls_bar(self):
        """
        Creates the top control bar with:
        - Load Data button
        - Precision label and spinbox
        """
        self.window.load_data_button = QPushButton('Load Data')
        self.window.load_data_button.setFixedSize(80, 25)

        self.window.precision_label = QLabel('Precision:')
        self.window.precision_spinbox = QSpinBox()
        self.window.precision_spinbox.setRange(1, 6)
        self.window.precision_spinbox.setValue(2)

        layout = QHBoxLayout()
        layout.addWidget(self.window.load_data_button)
        layout.addStretch()
        layout.addWidget(self.window.precision_label)
        layout.addWidget(self.window.precision_spinbox)
        return layout

    def create_nav_layout(self):
        """
        Creates navigation layout with:
        - Original button to revert to original data
        """
        layout = QHBoxLayout()
        self.window.original_button = QPushButton("Original")
        self.window.original_button.setEnabled(False)
        self.window.original_button.setMinimumHeight(30)
        self.window.original_button.clicked.connect(self.window.data_version_controller.original_data)
        layout.addWidget(self.window.original_button)
        return layout
