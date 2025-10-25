from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QCheckBox, QTabWidget
)
from typing import Any, Dict, Type
from utils import AppContext, EventBus, EventType, Event
from .graph_tabs.graph_tab import BaseGraphTab

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
    Uses EventBus for communication.
    """
    def __init__(
        self,
        context: AppContext,
        dist_selector_cls: Type,
        graph_tabs: Dict[str, BaseGraphTab]
    ):
        """
        Args:
            context: Application context with event_bus and data_model
            dist_selector_cls: Distribution selector widget class
            graph_tabs: Dictionary of {tab_name: tab_widget_instance}
        """
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.graph_tabs: Dict[str, BaseGraphTab] = graph_tabs

        self._init_controls(dist_selector_cls)
        self._init_tabs()
        self._setup_layout()
        self._connect_signals()
        self._subscribe_to_events()

    def _init_controls(self, dist_selector_cls) -> None:
        """Initialize UI controls."""
        self.controls_layout = QHBoxLayout()

        # bins control
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(MIN_BINS, MAX_BINS)
        self.bins_spinbox.setValue(DEFAULT_BINS)
        self.bins_spinbox.setMaximumWidth(MAX_BINS_SPINBOX_WIDTH)

        # confidence level
        self.confidence_spinbox = QDoubleSpinBox()
        self.confidence_spinbox.setRange(MIN_CONF, MAX_CONF)
        self.confidence_spinbox.setSingleStep(CONF_STEP)
        self.confidence_spinbox.setValue(DEFAULT_CONF)
        self.confidence_spinbox.setDecimals(CONF_PRECISION)

        # toggle checkboxes
        self.show_kde_checkbox = QCheckBox("Show curves")
        self.show_kde_checkbox.setChecked(False)
        
        self.show_line_checkbox = QCheckBox("Show broken lines")
        self.show_line_checkbox.setChecked(False)

        # assemble controls
        self.controls_layout.addWidget(QLabel("Bins:"))
        self.controls_layout.addWidget(self.bins_spinbox)
        self.controls_layout.addSpacing(20)
        self.controls_layout.addWidget(QLabel("Confidence:"))
        self.controls_layout.addWidget(self.confidence_spinbox)
        self.controls_layout.addStretch()
        self.controls_layout.addWidget(self.show_kde_checkbox)
        self.controls_layout.addWidget(self.show_line_checkbox)

        # distribution selector
        self.dist_selector = dist_selector_cls()

    def _init_tabs(self) -> None:
        """Initialize graph tabs from provided instances."""
        self.tabs = QTabWidget()
        for name, tab in self.graph_tabs.items():
            tab.set_panel(self)
            self.tabs.addTab(tab, name)

    def _setup_layout(self) -> None:
        """Setup main layout."""
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addLayout(self.controls_layout)
        layout.addWidget(self.dist_selector)
        self.setLayout(layout)

    def _connect_signals(self) -> None:
        """Connect control signals to event emissions."""
        self.bins_spinbox.valueChanged.connect(
            lambda value: self.event_bus.emit_type(EventType.BINS_CHANGED, value)
        )
        self.confidence_spinbox.valueChanged.connect(
            lambda value: self.event_bus.emit_type(EventType.CONFIDENCE_CHANGED, value)
        )
        self.show_kde_checkbox.stateChanged.connect(
            lambda: self.event_bus.emit_type(EventType.ADDITIONAL_GRAPH_TOGGLED)
        )
        self.show_line_checkbox.stateChanged.connect(
            lambda: self.event_bus.emit_type(EventType.ADDITIONAL_GRAPH_TOGGLED)
        )
        self.dist_selector.set_on_change(
            lambda: self.event_bus.emit_type(EventType.DISTRIBUTION_CHANGED)
        )

    def _subscribe_to_events(self) -> None:
        """Subscribe to relevant events."""
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_TRANSFORMED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.COLUMN_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.BINS_CHANGED, self._on_bins_changed)
        self.event_bus.subscribe(EventType.CONFIDENCE_CHANGED, self._on_render_params_changed)
        self.event_bus.subscribe(EventType.DISTRIBUTION_CHANGED, self._on_render_params_changed)
        self.event_bus.subscribe(EventType.ADDITIONAL_GRAPH_TOGGLED, self._on_render_params_changed)

    def _on_data_changed(self, event: Event) -> None:
        """Handle data changes."""
        data_model = self.context.data_model
        if data_model is None:
            self.clear()
            return
        
        # update bins spinbox maximum
        series = data_model.series
        if series is not None and not series.empty:
            self.bins_spinbox.setMaximum(len(series))
        
        self.refresh_all()

    def _on_bins_changed(self, event: Event) -> None:
        """Handle bins change."""
        bins = event.data
        data_model = self.context.data_model
        if data_model:
            data_model.update_bins(bins)
        self.refresh_all()

    def _on_render_params_changed(self, event: Event) -> None:
        """Handle rendering parameter changes."""
        self.refresh_all()

    def refresh_all(self) -> None:
        """Redraw all graphs with current data."""
        data_model = self.context.data_model
        if data_model is None:
            return

        series = data_model.series
        if series is None or series.empty:
            return

        clean_data = series.dropna()
        if clean_data.empty:
            return

        for tab in self.graph_tabs.values():
            tab.draw(clean_data)

    def clear(self) -> None:
        """Clear all graph tabs."""
        for tab in self.graph_tabs.values():
            tab.clear()

    def get_selected_distribution(self) -> Any:
        """Get currently selected distribution."""
        return self.dist_selector.get_selected_distribution()

    def get_render_params(self) -> dict[str, Any]:
        """
        Get current visualization parameters.
        Returns:
            Dictionary with bins, kde, line, confidence, distribution
        """
        return {
            "bins": self.bins_spinbox.value(),
            "kde": self.show_kde_checkbox.isChecked(),
            "line": self.show_line_checkbox.isChecked(),
            "confidence": self.confidence_spinbox.value(),
            "distribution": self.get_selected_distribution()
        }