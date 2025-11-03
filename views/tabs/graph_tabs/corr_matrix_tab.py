from .graph_tab import BaseGraphTab
from typing import Callable
from controllers import CorrelationController
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext, EventBus, EventType, Event


class CorrelationMatrixTab(BaseGraphTab):
    """Tab for correlation matrix visualization"""
    def __init__(self, context: AppContext, controller: CorrelationController):
        super().__init__(name="Correlation Matrix", context=context)
        self.controller: CorrelationController = controller
        self._cached_corr = None
        self.event_bus: EventBus = context.event_bus
        self._subscribe_to_events()

    def _subscribe_to_events(self):
        """Subscribe to relevant events."""
        self.event_bus.subscribe(EventType.CORR_COEFF_CHANGED, self._on_corr_changed)

    def _on_corr_changed(self, event: Event) -> None:
        """Handle rendering parameter changes."""
        corr_coef_name = event.data
        self._cached_corr = corr_coef_name
        self.draw()
        
    def draw(self):
        """Draw correlation matrix using selected correlation coeficient"""
        self.clear()
        data_model = self.context.data_model
        if self.panel is None or data_model is None: return

        dataframe = data_model.dataframe
        if dataframe is None: return
        
        # Render corr matrix
        renderer = RENDERERS['correlation_matrix']
        renderer.render(
            self.ax,
            dataframe,
            self.controller.calculate,
            self._cached_corr,
        )
        # styling
        self.apply_default_style(self.ax, "X", "Y")
        self.canvas.draw()