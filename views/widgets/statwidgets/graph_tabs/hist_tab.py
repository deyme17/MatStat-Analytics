from .graph_tab import BaseGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS

LEGEND_FRAMEALPHA = 0.5

class HistogramTab(BaseGraphTab):
    """Tab for histogram visualization"""
    def __init__(self, controller, get_data_model=None):
        super().__init__("Histogram", controller)
        
    def draw(self, data):
        """Draw histogram with current settings and distribution overlay"""
        self.clear()
        panel = self.panel
        params = panel.get_render_params()
        
        # Render histogram
        renderer = RENDERERS['histogram']
        renderer.render(
            self.ax, 
            data,
            bins=params['bins'],
            show_kde=params['kde'],
            freq_polygon=params['line']
        )
        
        # Draw distribution overlay if selected
        self._draw_distribution_overlay(data, params)
        
        # Apply styling
        self.apply_default_style(self.ax, "Value", "Frequency")
        self.canvas.draw()

    def _draw_distribution_overlay(self, data, params):
        """Draw theoretical distribution curve over the histogram."""
        dist = params["distribution"]
        if dist is None or data.isna().sum() > 0:
            return

        try:
            renderer = RENDERERS['distribution']
            renderer.render(
                self.ax,
                data,
                dist,
                bins=params['bins']
            )
            self.ax.legend(framealpha=LEGEND_FRAMEALPHA)
        except Exception as e:
            print(f"Distribution Error: {e}")