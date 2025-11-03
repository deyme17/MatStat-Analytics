from .graph_tab import BaseGraphTab
from typing import Callable
from controllers import CorrelationController
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext


class CorrelationMatrixTab(BaseGraphTab):
    """Tab for correlation matrix visualization"""
    def __init__(self, context: AppContext, controller: CorrelationController, 
                 get_corr_coef: Callable[[None], str]):
        super().__init__(name="Correlation Matrix", context=context)
        self.controller: CorrelationController = controller
        self.get_corr_coef: Callable[[None], str] = get_corr_coef
        
    def draw(self):
        """Draw correlation matrix using selected correlation coeficient"""
        self.clear()
        if self.panel is None: return
            
        dataframe = self.context.data_model.dataframe
        corr_coef_name = self.get_corr_coef()
        
        # Render corr matrix
        renderer = RENDERERS['correlation_matrix']
        renderer.render(
            self.ax,
            dataframe,
            self.controller.calculate,
            corr_coef_name,
        )
        # styling
        self.apply_default_style(self.ax, "Value", "Frequency")
        self.canvas.draw()