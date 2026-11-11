from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QRadioButton, QButtonGroup, QGroupBox
)
from PyQt6.QtCore import pyqtSignal


class PCAParamsWidget(QGroupBox):
    """Widget managing component selection mode and parameter inputs."""
    mode_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Component Selection Mode", parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Build parameter input layout."""
        layout = QVBoxLayout(self)

        radio_row = QHBoxLayout()
        self.radio_n = QRadioButton("Number of Components")
        self.radio_ev = QRadioButton("Variance Threshold")
        self.radio_n.setChecked(True)

        self._radio_group = QButtonGroup(self)
        self._radio_group.addButton(self.radio_n)
        self._radio_group.addButton(self.radio_ev)
        self._radio_group.buttonClicked.connect(self._on_mode_toggled)

        radio_row.addWidget(self.radio_n)
        radio_row.addWidget(self.radio_ev)
        radio_row.addStretch()
        layout.addLayout(radio_row)

        param_row = QHBoxLayout()
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setMinimum(1)
        self.n_spinbox.setValue(2)
        self.n_spinbox.setFixedWidth(50)

        self.ev_spinbox = QDoubleSpinBox()
        self.ev_spinbox.setRange(0.01, 1.0)
        self.ev_spinbox.setSingleStep(0.05)
        self.ev_spinbox.setValue(0.90)
        self.ev_spinbox.setDecimals(2)
        self.ev_spinbox.setFixedWidth(50)

        param_row.addWidget(QLabel("n_components:"))
        param_row.addWidget(self.n_spinbox)
        param_row.addSpacing(20)
        param_row.addWidget(QLabel("ev_threshold:"))
        param_row.addWidget(self.ev_spinbox)
        param_row.addStretch()

        layout.addLayout(param_row)
        self._on_mode_toggled()

    def _on_mode_toggled(self) -> None:
        """Toggle spinbox controls based on selection mode."""
        n_mode = self.radio_n.isChecked()
        self.n_spinbox.setEnabled(n_mode)
        self.ev_spinbox.setEnabled(not n_mode)
        self.mode_changed.emit()

    def set_max_components(self, count: int) -> None:
        """Set maximum allowable components."""
        self.n_spinbox.setMaximum(count)

    def get_params(self) -> tuple[int | None, float | None]:
        """Return (n_components, ev_threshold) based on selection."""
        if self.radio_n.isChecked():
            return self.n_spinbox.value(), None
        return None, self.ev_spinbox.value()