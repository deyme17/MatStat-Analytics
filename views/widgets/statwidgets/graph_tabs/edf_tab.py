from .graph_tab import BaseGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS

class EDFTab(BaseGraphTab):
    """Tab for Empirical Distribution Function (EDF) visualization"""
    
    def __init__(self):
        super().__init__("Empirical Distribution Function")

    def draw(self, data):
        """Draw EDF and overlay theoretical CDF with CI"""
        self.clear()
        panel = self.panel
        params = panel.get_render_params()

        # render
        renderer = RENDERERS['edf']
        model = panel.window.data_model

        renderer.render(
            self.ax,
            data,
            bin_edges=model.hist.bin_edges,
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
        if dist is None or data.isna().sum() > 0:
            return

        try:
            conf_service = self.panel.confidence_service
            result = conf_service.cdf_variance_ci(
                data, 
                dist, 
                params["confidence"]
            )
            
            if result:
                x_vals, cdf_vals, lower_ci, upper_ci = result
                self.ax.plot(x_vals, cdf_vals, '-', 
                            color=dist.color, 
                            label=f'{dist.name} CDF', 
                            linewidth=2)
                self.ax.fill_between(x_vals, lower_ci, upper_ci, 
                                   color='pink', alpha=0.2,
                                   label=f"Confidence level: {params['confidence'] * 100:.0f}%")
                self.ax.legend()
                self.ax.set_title("EDF and Statistical CDF with Confidence Interval")
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, 
                        f"Error plotting CDF: {str(e)}",
                        ha='center', va='center', 
                        transform=self.ax.transAxes)
