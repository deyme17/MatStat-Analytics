from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QSpinBox, QWidget
from typing import NamedTuple


class ControlsBar(NamedTuple):
    layout: QHBoxLayout
    load_button: QPushButton
    precision_spinbox: QSpinBox


class WindowWidgets:
    """
    Factory for building window-level widgets (controls bar, etc).
    """
    @staticmethod
    def create_controls_bar() -> ControlsBar:
        """
        Creates the top control bar with:
        - Load Data button
        - Precision label and spinbox

        Returns:
            ControlsBar: named tuple containing layout and individual widgets
        """
        load_data_button = QPushButton('Load Data')
        load_data_button.setFixedSize(80, 25)

        precision_label = QLabel('Precision:')
        precision_spinbox = QSpinBox()
        precision_spinbox.setRange(1, 6)
        precision_spinbox.setValue(2)

        layout = QHBoxLayout()
        layout.addWidget(load_data_button)
        layout.addStretch()
        layout.addWidget(precision_label)
        layout.addWidget(precision_spinbox)

        return ControlsBar(layout, load_data_button, precision_spinbox)