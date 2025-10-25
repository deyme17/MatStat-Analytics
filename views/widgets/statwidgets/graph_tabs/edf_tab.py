from .graph_tab import BaseGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS
from services import ConfidenceService
from utils import AppContext

LINEWIDTH = 2
CI_ALPHA = 0.2
CI_COLOR = 'pink'


class EDFTab(BaseGraphTab):
    """Tab for Empirical Distribution Function (EDF) visualization"""
    def __init__(self, context: AppContext, confidence_service: ConfidenceService):
        super().__init__(name="Empirical Distribution Function", context=context)
        self.confidence_service: ConfidenceService = confidence_service

    def draw(self, data):
        """Draw EDF and overlay theoretical CDF with CI"""
        self.clear()
        if self.panel is None: return
            
        params = self.panel.get_render_params()

        # get bin edges from data model
        data_model = self.get_data_model()
        if data_model is None or data_model.hist is None:
            return
            
        bin_edges = data_model.hist.bin_edges

        # Render EDF
        renderer = RENDERERS['edf']
        renderer.render(
            self.ax,
            data,
            bin_edges=bin_edges,
            show_edf_curve=params["kde"],
            show_ogiva=params["line"]
        )

        # draw theoretical CDF if distribution selected
        self._draw_theoretical_cdf(data, params)

        # styling
        self.apply_default_style(self.ax, "Value", "Cumulative Probability")
        self.ax.set_ylim(-0.05, 1.05)
        self.canvas.draw()

    def _draw_theoretical_cdf(self, data, params):
        """Draw theoretical CDF with confidence interval if possible."""
        dist = params["distribution"]
        if dist is None or data.isna().sum() > 0:
            return

        try:
            # compute CDF with confidence interval using service
            result = self.confidence_service.cdf_variance_ci(
                data, 
                dist, 
                params["confidence"]
            )
            
            if result:
                x_vals, cdf_vals, lower_ci, upper_ci = result
                
                # plot theoretical CDF
                self.ax.plot(
                    x_vals, cdf_vals, '-', 
                    color=dist.color, 
                    label=f'{dist.name} CDF', 
                    linewidth=LINEWIDTH
                )
                # plot confidence interval
                self.ax.fill_between(
                    x_vals, lower_ci, upper_ci, 
                    color=CI_COLOR, 
                    alpha=CI_ALPHA,
                    label=f"Confidence level: {params['confidence'] * 100:.0f}%"
                )
                
                self.ax.legend()
                self.ax.set_title("EDF and Statistical CDF with Confidence Interval")
                
        except Exception as e:
            self.ax.clear()
            self.ax.text(
                0.5, 0.5, 
                f"Error plotting CDF: {str(e)}",
                ha='center', va='center', 
                transform=self.ax.transAxes
            )
            self.canvas.draw()