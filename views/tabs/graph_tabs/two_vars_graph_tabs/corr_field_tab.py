from .base_2varGraph_tab import Base2VarGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext


class CorrelationFieldTab(Base2VarGraphTab):
    """Tab for correlation field visualization"""
    def __init__(self, context: AppContext):
        super().__init__(name="Correlation Field", context=context)
    
    def draw(self):
        """Draw correlation field for two columns"""
        self.clear()
        try:
            col1, col2 = self.get_current_column_names()
            renderer = RENDERERS['correlation_field']
            renderer.render(self.ax, self.context.data_model.dataframe, col1, col2)
            self.apply_default_style(self.ax, col1, col2)
            self.canvas.draw()
        except Exception as e:
            print(f"Correlation Field Error: {e}")
            self.clear()