from .graph_tab import BaseGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext
import pandas as pd

LEGEND_FRAMEALPHA = 0.5


class HHTab(BaseGraphTab):
    """Tab for H-H plot visualization"""
    def __init__(self, context: AppContext):
        super().__init__(name="H-H plot", context=context)
        
    def draw(self):
        """Draw H-H plot for selected theoretical distribution"""
        self.clear()
        if self.panel is None: return

        params = self.panel.get_render_params()
        series = self.context.data_model.series
        dist = params.get("distribution")

        if (dist is None) or (series is None) or (series.dropna().empty):
            return
        try:
            renderer = RENDERERS["hh_plot"]
            success = renderer.render(
                self.ax,
                data=series,
                dist=dist
            )
            if success:
                self.apply_default_style(self.ax, "Theoretical Quantiles", "Empirical Quantiles")
                self.ax.legend(framealpha=LEGEND_FRAMEALPHA)
                self.canvas.draw()
        except Exception as e:
            print(f"[HHTab] Error while rendering: {e}")