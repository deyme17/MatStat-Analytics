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
            data_model = self.get_data_model()
            if data_model is None or data_model.dataframe is None or data_model.dataframe.empty:
                return
            columns = self.get_current_column_names()
            if columns is None:
                return
            col1, col2 = columns
            if not col1 or not col2:
                return
            
            renderer = RENDERERS['correlation_field']
            renderer.render(self.ax, data_model.dataframe, col1, col2)
            self.apply_default_style(self.ax, col1, col2)
            self.canvas.draw()
        except Exception as e:
            print(f"Correlation Field Error: {e}")
            self.clear()