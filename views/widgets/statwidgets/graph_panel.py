from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QCheckBox, QTabWidget
)
from views.widgets.statwidgets.graph_tabs import registered_graphs
from typing import Callable, Optional, Any
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
        dist_selector_cls,
        graph_controller,
        get_data_model: Callable[[], Any],
    ):
        """
        Args:
            dist_selector_cls: Distribution selector widget class
            graph_controller: Controller for graph operations and computations
            get_data_model: Function for getting current DataModel
        """
        super().__init__()
        self.data = None
        self.graph_controller = graph_controller
        self.graph_tabs = {}

        self._init_controls(dist_selector_cls)

        self.tabs = QTabWidget()
        for name, tab_cls in registered_graphs.items():
            tab = tab_cls(self.graph_controller, get_data_model)
            tab.set_context(self)
            self.tabs.addTab(tab, name)
            self.graph_tabs[name] = tab

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addLayout(self.controls_layout)
        layout.addWidget(self.dist_selector)
        self.setLayout(layout)

    def _init_controls(self, dist_selector_cls) -> None:
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

        # curve toggle
        self.show_kde_checkbox = QCheckBox("Show curves")
        self.show_kde_checkbox.setChecked(False)
        # KDE toggle
        self.show_line_checkbox = QCheckBox("Show broken lines")
        self.show_line_checkbox.setChecked(False)

        # Assemble controls
        self.controls_layout.addWidget(QLabel("Bins:"))
        self.controls_layout.addWidget(self.bins_spinbox)
        self.controls_layout.addSpacing(20)
        self.controls_layout.addWidget(QLabel("Confidence:"))
        self.controls_layout.addWidget(self.confidence_spinbox)
        self.controls_layout.addStretch()
        self.controls_layout.addWidget(self.show_kde_checkbox)
        self.controls_layout.addWidget(self.show_line_checkbox)

        # Distribution selector
        self.dist_selector = dist_selector_cls()

    def connect_controls(self) -> None:
        """Connect control signals to callbacks."""
        self.bins_spinbox.valueChanged.connect(self.graph_controller.on_bins_changed)
        self.confidence_spinbox.valueChanged.connect(self.graph_controller.on_alpha_changed)
        self.show_kde_checkbox.stateChanged.connect(self.graph_controller.on_kde_toggled)
        self.show_line_checkbox.stateChanged.connect(self.graph_controller.on_line_toggled)
        self.dist_selector.set_on_change(self.graph_controller.on_distribution_changed)

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

    def get_selected_distribution(self) -> Optional[Any]:
        """Get currently selected distribution."""
        return self.dist_selector.get_selected_distribution()

    def get_render_params(self) -> dict[str, Any]:
        """
        Get current visualization parameters.
        Returns:
            Dictionary with:
            - bins: int
            - kde: bool
            - confidence: float
            - distribution: StatisticalDistribution
        """
        return {
            "bins": self.bins_spinbox.value(),
            "kde": self.show_kde_checkbox.isChecked(),
            "line": self.show_line_checkbox.isChecked(),
            "confidence": self.confidence_spinbox.value(),
            "distribution": self.get_selected_distribution()
        }