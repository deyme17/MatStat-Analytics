from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QCheckBox, QTabWidget
)
from views.widgets.statwidgets.graph_tabs import registered_graphs
from typing import Callable, Dict, Optional, Any
import pandas as pd

MIN_BINS, MAX_BINS = 1, 999
DEFAULT_BINS = 10
MAX_BINS_SPINBOX_WIDTH = 100

MIN_CONF, MAX_CONF = 0.80, 0.99
CONF_STEP = 0.01
DEFAULT_CONF = 0.95
CONF_PRECISION = 2


class GraphPanel(QWidget):
    """
    Visualization panel hosting graph tabs and controls.
    Completely decoupled from main window.
    """

    def __init__(
        self,
        dist_selector_cls: type,
        on_bins_changed: Callable[[int], None],
        on_alpha_changed: Callable[[float], None],
        on_kde_toggled: Callable[[bool], None],
        on_dist_changed: Callable[[object], None],
    ):
        """
        Args:
            dist_selector_cls: Distribution selector widget class
            on_bins_changed: Callback for bin count changes
            on_alpha_changed: Callback for confidence level changes
            on_kde_toggled: Callback for KDE toggle
            on_dist_changed: Callback for distribution selection
        """
        super().__init__()
        self.data = None
        self.graph_tabs = {}
        self._callbacks = {
            'bins': on_bins_changed,
            'alpha': on_alpha_changed,
            'kde': on_kde_toggled,
            'dist': on_dist_changed
        }

        self._init_controls(dist_selector_cls)
        self._connect_controls()

        self.tabs = QTabWidget()
        for name, tab_cls in registered_graphs.items():
            tab = tab_cls()
            tab.set_context(self)
            self.tabs.addTab(tab, name)
            self.graph_tabs[name] = tab

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addLayout(self.controls_layout)
        layout.addWidget(self.dist_selector)
        self.setLayout(layout)

    def _init_controls(self, dist_selector_cls: type) -> None:
        """Initialize UI controls."""
        self.controls_layout = QHBoxLayout()

        # Bins control
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(MIN_BINS, MAX_BINS)
        self.bins_spinbox.setValue(DEFAULT_BINS)
        self.bins_spinbox.setMaximumWidth(MAX_BINS_SPINBOX_WIDTH)

        # Confidence level
        self.confidence_spinbox = QDoubleSpinBox()
        self.confidence_spinbox.setRange(MIN_CONF, MAX_CONF)
        self.confidence_spinbox.setSingleStep(CONF_STEP)
        self.confidence_spinbox.setValue(DEFAULT_CONF)
        self.confidence_spinbox.setDecimals(CONF_PRECISION)

        # KDE toggle
        self.show_kde_checkbox = QCheckBox("Show KDE")
        self.show_kde_checkbox.setChecked(False)

        # Assemble controls
        self.controls_layout.addWidget(QLabel("Bins:"))
        self.controls_layout.addWidget(self.bins_spinbox)
        self.controls_layout.addSpacing(20)
        self.controls_layout.addWidget(QLabel("Confidence:"))
        self.controls_layout.addWidget(self.confidence_spinbox)
        self.controls_layout.addStretch()
        self.controls_layout.addWidget(self.show_kde_checkbox)

        # Distribution selector
        self.dist_selector = dist_selector_cls()

    def _connect_controls(self) -> None:
        """Connect control signals to callbacks."""
        self.bins_spinbox.valueChanged.connect(self._callbacks['bins'])
        self.confidence_spinbox.valueChanged.connect(self._callbacks['alpha'])
        self.show_kde_checkbox.stateChanged.connect(
            lambda state: self._callbacks['kde'](state == 2)  # Qt.Checked
        )
        self.dist_selector.set_on_change(self._callbacks['dist'])

    def set_data(self, data: pd.Series) -> None:
        """
        Set data for visualization.
        
        Args:
            data: Input data series
        """
        self.data = data
        if data is not None:
            self.bins_spinbox.setMaximum(len(data))

    def refresh_all(self) -> None:
        """Redraw all graphs with current data."""
        if self.data is None or self.data.empty:
            return

        clean_data = self.data.dropna()
        if clean_data.empty:
            return

        for tab in self.graph_tabs.values():
            tab.draw(clean_data)

    def clear(self) -> None:
        """Clear all graph tabs."""
        for tab in self.graph_tabs.values():
            tab.clear()

    def get_selected_distribution(self) -> Optional[object]:
        """Get currently selected distribution."""
        return self.dist_selector.get_selected_distribution()

    def get_render_params(self) -> Dict[str, Any]:
        """
        Get current visualization parameters.
        
        Returns:
            Dictionary with:
            - bins: int
            - kde: bool
            - confidence: float
            - distribution: object
        """
        return {
            "bins": self.bins_spinbox.value(),
            "kde": self.show_kde_checkbox.isChecked(),
            "confidence": self.confidence_spinbox.value(),
            "distribution": self.get_selected_distribution()
        }