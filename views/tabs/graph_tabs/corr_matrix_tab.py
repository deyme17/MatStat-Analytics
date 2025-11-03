from .graph_tab import BaseGraphTab
from models.correlation_coeffs import ICorrelationCoefficient
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext


class CorrelationMatrixTab(BaseGraphTab):
    """Tab for correlation matrix visualization"""
    def __init__(self, context: AppContext, get_corr_coef: callable[[None], ICorrelationCoefficient]):
        super().__init__(name="Correlation Matrix", context=context)
        self.get_corr_coef: callable[[None], ICorrelationCoefficient] = get_corr_coef
        
    def draw(self):
        """Draw correlation matrix using selected correlation coeficient"""
        self.clear()
        if self.panel is None: return
            
        dataframe = self.context.data_model.dataframe
        corr_coef = self.get_corr_coef()
        
        # Render corr matrix
        renderer = RENDERERS['correlation_matrix']
        renderer.render(
            self.ax,
            dataframe,
            corr_coef.fit,
            corr_coef.name(),
        )
        
        # styling
        self.apply_default_style(self.ax, "Value", "Frequency")
        self.canvas.draw()