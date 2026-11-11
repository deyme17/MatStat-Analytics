from typing import Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import QTimer
from utils import AppContext, EventBus, EventType, Event
from views.tabs.graph_tabs.graph_tab import BaseGraphTab
from views.widgets.windowwidgets.dist_selector import DistributionSelector
from views.widgets.windowwidgets.subwidgets import GraphControlsWidget

PANEL_HEIGHT = 700
PANEL_WIDTH = 990
RENDER_DELAY_MS = 250


class GraphPanel(QWidget):
    """Visualization panel hosting graph tabs, control bar, and distribution selector."""
    def __init__(self, 
                 context: AppContext, 
                 dist_selector: DistributionSelector, 
                 graph_tabs: dict[str, BaseGraphTab]):
        super().__init__()
        self.dist_selector = dist_selector
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.graph_tabs: dict[str, BaseGraphTab] = graph_tabs

        # timer
        self.render_timer = QTimer()
        self.render_timer.setSingleShot(True)
        self.render_timer.timeout.connect(self.refresh_all)

        self._init_ui()
        self._connect_signals()
        self._subscribe_to_events()

    def _init_ui(self) -> None:
        """Initialize UI structure, control bar, and tabs layout."""
        layout = QVBoxLayout(self)

        self.control_bar = GraphControlsWidget()
        self.tabs = QTabWidget()

        for name, tab in self.graph_tabs.items():
            tab.set_panel(self)
            self.tabs.addTab(tab, name)

        layout.addWidget(self.tabs)
        layout.addWidget(self.control_bar)
        layout.addWidget(self.dist_selector)

        self.setFixedSize(PANEL_WIDTH, PANEL_HEIGHT)

    def _connect_signals(self) -> None:
        """Connect UI control signals to EventBus emissions."""
        self.tabs.currentChanged.connect(self._on_tab_changed)

        self.control_bar.bins_spinbox.valueChanged.connect(
            lambda value: self.event_bus.emit_type(EventType.BINS_CHANGED, value)
        )
        self.control_bar.confidence_spinbox.valueChanged.connect(
            lambda value: self.event_bus.emit_type(EventType.CONFIDENCE_CHANGED, value)
        )
        self.control_bar.show_kde_checkbox.stateChanged.connect(
            lambda: self.event_bus.emit_type(EventType.ADDITIONAL_GRAPH_TOGGLED)
        )
        self.control_bar.show_line_checkbox.stateChanged.connect(
            lambda: self.event_bus.emit_type(EventType.ADDITIONAL_GRAPH_TOGGLED)
        )
        self.dist_selector.set_on_change(
            lambda: self.event_bus.emit_type(EventType.DISTRIBUTION_CHANGED)
        )

    def _subscribe_to_events(self) -> None:
        """Subscribe to relevant EventBus events."""
        self.event_bus.subscribe(EventType.MISSING_VALUES_DETECTED, self._on_missings)
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_TRANSFORMED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.COLUMN_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.BINS_CHANGED, self._on_bins_changed)
        self.event_bus.subscribe(EventType.CONFIDENCE_CHANGED, self._request_render)
        self.event_bus.subscribe(EventType.DISTRIBUTION_CHANGED, self._request_render)
        self.event_bus.subscribe(EventType.ADDITIONAL_GRAPH_TOGGLED, self._request_render)

    def _on_tab_changed(self, index: int) -> None:
        """Draw active tab content on tab switch."""
        active_tab = self.tabs.widget(index)
        if active_tab:
            self.refresh_all()

    def _request_render(self, event: Event | None = None) -> None:
        """Start debounce timer for render request."""
        self.render_timer.start(RENDER_DELAY_MS)

    def _on_data_changed(self, event: Event) -> None:
        """Handle data model state changes."""
        data_model = self.context.data_model
        if data_model is None:
            self.clear()
            return

        series = data_model.series
        if series is not None and not series.empty:
            self.control_bar.set_max_bins(len(series))

        self.refresh_all()

    def _on_bins_changed(self, event: Event) -> None:
        """Handle changes in bins count."""
        bins = event.data
        data_model = self.context.data_model
        if data_model:
            data_model.update_bins(bins)
        self._request_render()

    def _on_missings(self, event: Event) -> None:
        """Clear graphs when missing values exist in dataset."""
        self.clear()

    def refresh_all(self) -> None:
        """Redraw only the active graph tab."""
        data_model = self.context.data_model
        if data_model is None:
            return
        series = data_model.series
        if (series is None or series.empty or data_model.dataframe.isna().any().any()):
            return

        active_tab = self.tabs.currentWidget()
        if active_tab and hasattr(active_tab, 'draw'):
            active_tab.draw()

    def clear(self) -> None:
        """Clear graph output across all registered tabs."""
        for tab in self.graph_tabs.values():
            tab.clear()

    def get_render_params(self) -> dict[str, Any]:
        """
        Get combined visualization parameters from control bar and distribution selector.
        """
        params = self.control_bar.get_control_params()
        params["distribution"] = self.dist_selector.get_selected_distribution()
        return params
    
    def get_bins(self) -> int:
        """Get current bins value from control bar."""
        return self.control_bar.get_control_params()["bins"]

    def get_confidence(self) -> float:
        """Get current confidence value from control bar."""
        return self.control_bar.get_control_params()["confidence"]

    def set_bins(self, value: int) -> None:
        """Set bins value in control bar."""
        self.control_bar.bins_spinbox.setValue(value)