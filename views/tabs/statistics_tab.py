from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QHeaderView
from services.ui_services.renderers.table_renderers import (
    StatsRenderer, VarSerRenderer, MultiVarRenderer
)
from utils import EventBus, EventType, Event


class StatisticsTab(QWidget):
    """
    A QWidget tab displaying a table of confidence intervals
    for statistical summaries and variation series.
    """
    def __init__(self, event_bus: EventBus, parent=None):
        super().__init__(parent)
        self.event_bus: EventBus = event_bus
        self._init_ui()
        self._subscribe_to_events()

    def _init_ui(self) -> None:
        self._layout = QVBoxLayout(self)

        self.conf_label = QLabel("Confidence Intervals Table")
        self.conf_table = QTableWidget()
        self.conf_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._layout.addWidget(self.conf_label)
        self._layout.addWidget(self.conf_table)
        self.stat_renderer = StatsRenderer(self.conf_table)

        self.var_label = QLabel("Variation Series Table")
        self.var_table = QTableWidget()
        self.var_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._layout.addWidget(self.var_label)
        self._layout.addWidget(self.var_table)
        self.var_renderer = VarSerRenderer(self.var_table)

        self.multi_label = QLabel("Multivariable Table")
        self.multi_table = QTableWidget()
        self.multi_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._layout.addWidget(self.multi_label)
        self._layout.addWidget(self.multi_table)
        self.multi_renderer = MultiVarRenderer(self.multi_table)

    def _subscribe_to_events(self) -> None:
        """Subscribe tab to calculated statistics payload events."""
        self.event_bus.subscribe(EventType.STATS_UPDATED, self._on_stats_updated)
        self.event_bus.subscribe(EventType.STATS_CLEARED, self._on_stats_cleared)

    def _on_stats_updated(self, event: Event) -> None:
        """Render received statistical calculations."""
        payload = event.data
        if not payload:
            return

        precision = payload["precision"]
        self.stat_renderer.render(payload["stats"], payload["ci"], precision=precision)
        self.var_renderer.render(payload["var_series"])
        self.multi_renderer.render(payload["multi_var"], precision=precision)

    def _on_stats_cleared(self, event: Event) -> None:
        """Clear headers and content."""
        self.stat_renderer._setup_headers()
        self.var_renderer._setup_headers()
        self.multi_renderer._setup_headers()