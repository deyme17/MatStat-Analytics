from ..graph_tab import BaseGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext


class ParallelCoordsTab(BaseGraphTab):
    """Tab for parallel coordinates visualization"""
    def __init__(self, context: AppContext):
        super().__init__(name="Parallel Coordinates", context=context)

    def draw(self):
        """Draw parallel coordinates plot for multivariate data visualization."""
        self.clear()
        data_model = self.context.data_model
        if self.panel is None or data_model is None:
            return
        dataframe = data_model.dataframe
        if dataframe is None:
            return

        renderer = RENDERERS['parallel_coordinates']
        renderer.render(
            self.ax,
            dataframe,
        )
        self.apply_default_style(self.ax, "", "")
        self.canvas.draw()