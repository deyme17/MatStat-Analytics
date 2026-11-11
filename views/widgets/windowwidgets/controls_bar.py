from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QSpinBox
from typing import NamedTuple, Callable

DEFAULT_PRECISION_VAL = 2
MIN_PRECISION, MAX_PRECISION = 1, 6
LOAD_BUTTON_WIDTH, LOAD_BUTTON_HEIGHT = 80, 25


class ControlsBar(NamedTuple):
    layout: QHBoxLayout
    load_button: QPushButton
    precision_spinbox: QSpinBox

    def get_precision(self) -> int:
        """Get current precision value."""
        return self.precision_spinbox.value()

    def on_load_clicked(self, callback: Callable[[], None]) -> None:
        """Connect callback to Load Data button click event."""
        self.load_button.clicked.connect(callback)

    def on_precision_changed(self, callback: Callable[[int], None]) -> None:
        """Connect callback to precision spinbox value change event."""
        self.precision_spinbox.valueChanged.connect(callback)


class ControlsBarWidget:
    """Factory for building window-level control bar widget."""
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
        load_data_button.setFixedSize(LOAD_BUTTON_WIDTH, LOAD_BUTTON_HEIGHT)

        precision_label = QLabel('Precision:')
        precision_spinbox = QSpinBox()
        precision_spinbox.setRange(MIN_PRECISION, MAX_PRECISION)
        precision_spinbox.setValue(DEFAULT_PRECISION_VAL)

        layout = QHBoxLayout()
        layout.addWidget(load_data_button)
        layout.addStretch()
        layout.addWidget(precision_label)
        layout.addWidget(precision_spinbox)

        return ControlsBar(layout, load_data_button, precision_spinbox)