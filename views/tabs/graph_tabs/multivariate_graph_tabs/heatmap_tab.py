from ..graph_tab import BaseGraphTab
from controllers import CorrelationController
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext, EventBus, EventType, Event
from PyQt6.QtWidgets import QCheckBox


class HeatMapTab(BaseGraphTab):
    """Tab for heat map visualization"""
    def __init__(self, context: AppContext):
        super().__init__(name="Heat Map", context=context)

    def draw(self):
        """Draw correlation matrix using selected correlation coefficient."""
        self.clear()
        data_model = self.context.data_model
        if self.panel is None or data_model is None:
            return
        dataframe = data_model.dataframe
        if dataframe is None:
            return

        renderer = RENDERERS['heatmap']
        renderer.render(
            self.ax,
            dataframe,
        )
        self.apply_default_style(self.ax, "", "")
        self.canvas.draw()