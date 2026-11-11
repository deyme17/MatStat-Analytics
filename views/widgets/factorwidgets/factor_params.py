from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QRadioButton, QButtonGroup, QGroupBox
)
from PyQt6.QtCore import pyqtSignal


class FactorParamsWidget(QGroupBox):
    """Widget managing factor selection modes and inputs."""
    mode_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Factor Selection Mode", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize layout for factor selection."""
        layout = QVBoxLayout(self)

        radio_row = QHBoxLayout()
        self.radio_n = QRadioButton("Number of Factors")
        self.radio_auto = QRadioButton("Auto")
        self.radio_auto.setChecked(True)

        self._radio_group = QButtonGroup(self)
        self._radio_group.addButton(self.radio_n)
        self._radio_group.addButton(self.radio_auto)
        self._radio_group.buttonClicked.connect(self._on_mode_toggled)

        radio_row.addWidget(self.radio_n)
        radio_row.addWidget(self.radio_auto)
        radio_row.addStretch()
        layout.addLayout(radio_row)

        param_row = QHBoxLayout()
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setMinimum(1)
        self.n_spinbox.setValue(2)
        self.n_spinbox.setFixedWidth(50)

        param_row.addWidget(QLabel("n_factors:"))
        param_row.addWidget(self.n_spinbox)
        param_row.addStretch()

        layout.addLayout(param_row)
        self._on_mode_toggled()

    def _on_mode_toggled(self) -> None:
        """Toggle spinbox state based on radio selection."""
        self.n_spinbox.setEnabled(self.radio_n.isChecked())
        self.mode_changed.emit()

    def set_max_factors(self, max_val: int) -> None:
        """Set maximum allowable factors."""
        self.n_spinbox.setMaximum(max_val)

    def get_n_factors(self) -> int | None:
        """Return factor count if manual mode selected, else None."""
        return self.n_spinbox.value() if self.radio_n.isChecked() else None