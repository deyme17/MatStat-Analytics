from .base_trivariate_tab import Base3VarGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext


class CorreletionField3dTab(Base3VarGraphTab):
    """Tab for correletion field 3d visualization"""
    def __init__(self, context: AppContext):
        super().__init__(name="Correletion Field 3d", context=context, axis3d=True)
    
    def draw(self):
        """Draw correletion field 3d for three selected columns"""
        self.clear()
        try:
            data_model = self.get_data_model()
            if data_model is None or data_model.dataframe is None or data_model.dataframe.empty:
                return
            columns = self.get_current_column_names()
            if columns is None:
                return
            col1, col2, col3 = columns
            
            renderer = RENDERERS['correlation_field_3d']
            renderer.render(
                self.ax,
                data_model.dataframe,
                col1,
                col2,
                col3
            )
            self.apply_default_style(self.ax, col1, col2, col3)
            self.canvas.draw()
        except Exception as e:
            print(f"[CorreletionField3dTab] Error while rendering: {e}")