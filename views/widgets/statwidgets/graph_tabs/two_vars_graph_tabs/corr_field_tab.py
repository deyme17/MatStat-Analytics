from .base_2varGraph_tab import Base2VarGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext
import pandas as pd


class CorrelationFieldTab(Base2VarGraphTab):
    """Tab for correlation field visualization"""
    def __init__(self, context: AppContext):
        super().__init__(name="Correlation Field", context=context)
    
    def draw(self, df: pd.DataFrame, col_x: str, col_y: str):
        """Draw correlation field for two columns"""
        self.clear()
        try:
            renderer = RENDERERS['correlation_field']
            renderer.render(self.ax, df, col_x, col_y)
            self.apply_default_style(self.ax, col_x, col_y)
            self.canvas.draw()
        except Exception as e:
            print(f"Correlation Field Error: {e}")
            self.clear()