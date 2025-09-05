from .graph_tab import BaseGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS
from typing import Callable, Any

LINEWIDTH = 2
CI_ALPHA = 0.2
CI_COLOR = 'pink'

class EDFTab(BaseGraphTab):
    """Tab for Empirical Distribution Function (EDF) visualization"""
    def __init__(self, controller, get_data_model:  Callable[[], Any] = None):
        super().__init__("Empirical Distribution Function", controller, get_data_model)

    def draw(self, data):
        """Draw EDF and overlay theoretical CDF with CI"""
        self.clear()
        panel = self.panel
        params = panel.get_render_params()

        # render
        renderer = RENDERERS['edf']
        data_model = self.get_data_model()
        bin_edges = data_model.hist.bin_edges

        renderer.render(
            self.ax,
            data,
            bin_edges=bin_edges,
            show_edf_curve=params["kde"]
        )

        # cdf
        self._draw_theoretical_cdf(data, params)

        # style
        self.apply_default_style(self.ax, "Value", "Cumulative Probability")
        self.ax.set_ylim(-0.05, 1.05)
        self.canvas.draw()

    def _draw_theoretical_cdf(self, data, params):
        """Draw theoretical CDF with confidence interval if possible."""
        dist = params["distribution"]
        if dist is None or data.isna().sum() > 0 or not self.controller:
            return

        try:
            result = self.controller.compute_cdf_with_ci(
                data, dist, params["confidence"]
            )
            
            if result:
                x_vals, cdf_vals, lower_ci, upper_ci = result
                self.ax.plot(x_vals, cdf_vals, '-', 
                            color=dist.color, 
                            label=f'{dist.name} CDF', 
                            linewidth=LINEWIDTH)
                self.ax.fill_between(x_vals, lower_ci, upper_ci, 
                                   color=CI_COLOR, alpha=CI_ALPHA,
                                   label=f"Confidence level: {params['confidence'] * 100:.0f}%")
                self.ax.legend()
                self.ax.set_title("EDF and Statistical CDF with Confidence Interval")
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, 
                        f"Error plotting CDF: {str(e)}",
                        ha='center', va='center', 
                        transform=self.ax.transAxes)
