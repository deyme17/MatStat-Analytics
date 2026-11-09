from .base_trivariate_tab import Base3VarGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext


class BubblePlotTab(Base3VarGraphTab):
    """Tab for bubble plot visualization"""
    def __init__(self, context: AppContext):
        super().__init__(name="Bubble Plot", context=context)
    
    def draw(self):
        """Draw bubble plot for three selected columns"""
        self.clear()
        try:
            data_model = self.get_data_model()
            if data_model is None or data_model.dataframe is None or data_model.dataframe.empty:
                return
            columns = self.get_current_column_names()
            if columns is None:
                return
            col1, col2, col3 = columns
            
            renderer = RENDERERS['bubble_plot']
            renderer.render(
                self.ax,
                data_model.dataframe,
                col1,
                col2,
                col3
            )
            self.apply_default_style(self.ax, col1, col2)
            self.canvas.draw()
        except Exception as e:
            print(f"[BubblePlotTab] Error while rendering: {e}")