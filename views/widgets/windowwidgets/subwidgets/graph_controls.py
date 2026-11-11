from typing import Any
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox
from views.widgets.utils import make_checkbox, make_alpha_spinbox

MIN_BINS, MAX_BINS = 1, 999
DEFAULT_BINS = 10
MAX_BINS_SPINBOX_WIDTH = 100

MIN_CONF, MAX_CONF = 0.80, 0.99
CONF_STEP = 0.01
DEFAULT_CONF = 0.95
CONF_PRECISION = 2


class GraphControlsWidget(QWidget):
    """Subwidget hosting interactive control elements for graph rendering."""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize UI controls and layout."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # bins
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(MIN_BINS, MAX_BINS)
        self.bins_spinbox.setValue(DEFAULT_BINS)
        self.bins_spinbox.setMaximumWidth(MAX_BINS_SPINBOX_WIDTH)

        # conf level
        self.confidence_spinbox = make_alpha_spinbox(
            min_val=MIN_CONF,
            max_val=MAX_CONF,
            step=CONF_STEP,
            decimals=CONF_PRECISION,
            default=DEFAULT_CONF
        )

        # checkboxes
        self.show_kde_checkbox = make_checkbox("Show curves", checked=False)
        self.show_line_checkbox = make_checkbox("Show broken lines", checked=False)

        # layout
        layout.addWidget(QLabel("Bins:"))
        layout.addWidget(self.bins_spinbox)
        layout.addSpacing(20)
        layout.addWidget(QLabel("Confidence:"))
        layout.addWidget(self.confidence_spinbox)
        layout.addStretch()
        layout.addWidget(self.show_kde_checkbox)
        layout.addWidget(self.show_line_checkbox)

    def set_max_bins(self, max_bins: int) -> None:
        """Set upper boundary limit for bins spinbox."""
        self.bins_spinbox.setMaximum(max_bins)

    def get_control_params(self) -> dict[str, Any]:
        """Get current parameter values from control bar elements."""
        return {
            "bins": self.bins_spinbox.value(),
            "kde": self.show_kde_checkbox.isChecked(),
            "line": self.show_line_checkbox.isChecked(),
            "confidence": self.confidence_spinbox.value(),
        }