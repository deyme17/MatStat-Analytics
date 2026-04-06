from ..graph_tab import BaseGraphTab
from controllers import CorrelationController
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext, EventBus, EventType, Event
from PyQt6.QtWidgets import QCheckBox


class CorrelationMatrixTab(BaseGraphTab):
    """Tab for correlation matrix visualization"""
    def __init__(self, context: AppContext, controller: CorrelationController):
        super().__init__(name="Correlation Matrix", context=context)
        self.controller: CorrelationController = controller
        self._cached_corr = None
        self.event_bus: EventBus = context.event_bus
        self._add_significance_checkbox()
        self._subscribe_to_events()

    def _add_significance_checkbox(self) -> None:
        """Add significance filter checkbox at the bottom of the tab layout."""
        self._significant_only_cb = QCheckBox("Show only significant")
        self._significant_only_cb.setChecked(False)
        self._significant_only_cb.stateChanged.connect(self.draw)
        self.layout().addWidget(self._significant_only_cb)

    def _subscribe_to_events(self):
        """Subscribe to relevant events."""
        self.event_bus.subscribe(EventType.CORR_COEFF_CHANGED, self._on_corr_changed)

    def _on_corr_changed(self, event: Event) -> None:
        """Handle rendering parameter changes."""
        self._cached_corr = event.data
        self.draw()

    def draw(self):
        """Draw correlation matrix using selected correlation coefficient."""
        self.clear()
        data_model = self.context.data_model
        if self.panel is None or data_model is None:
            return

        dataframe = data_model.dataframe
        if dataframe is None:
            return

        renderer = RENDERERS['correlation_matrix']
        renderer.render(
            self.ax,
            dataframe,
            self.controller.calculate,
            self._cached_corr,
            significance_callable=(
                self.controller.test_significance
                if self._significant_only_cb.isChecked()
                else None
            ),
        )
        self.apply_default_style(self.ax, "", "")
        self.canvas.draw()