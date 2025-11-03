from .graph_tab import BaseGraphTab
from typing import Callable
from controllers import CorrelationController
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext, EventBus, EventType, Event


class CorrelationMatrixTab(BaseGraphTab):
    """Tab for correlation matrix visualization"""
    def __init__(self, context: AppContext, controller: CorrelationController, 
                 get_corr_coef: Callable[[None], str]):
        super().__init__(name="Correlation Matrix", context=context)
        self.controller: CorrelationController = controller
        self.get_corr_coef: Callable[[None], str] = get_corr_coef
        self.event_bus: EventBus = context.event_bus
        self._subscribe_to_events()

    def _subscribe_to_events(self):
        """Subscribe to relevant events."""
        self.event_bus.subscribe(EventType.CORR_COEFF_CHANGED, self._on_corr_changed)

    def _on_corr_changed(self, event: Event) -> None:
        """Handle rendering parameter changes."""
        corr_coef_name = event.data
        self.draw(corr_coef_name)
        
    def draw(self, corr_coef_name: str = None):
        """Draw correlation matrix using selected correlation coeficient"""
        self.clear()
        if self.panel is None: return
            
        dataframe = self.context.data_model.dataframe
        corr_coef_name = self.get_corr_coef() if not corr_coef_name else corr_coef_name
        
        # Render corr matrix
        renderer = RENDERERS['correlation_matrix']
        renderer.render(
            self.ax,
            dataframe,
            self.controller.calculate,
            corr_coef_name,
        )
        # styling
        self.apply_default_style(self.ax, "X", "Y")
        self.canvas.draw()