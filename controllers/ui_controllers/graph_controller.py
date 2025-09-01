from typing import Callable
import pandas as pd

class GraphController:
    """
    Controller for coordinating plotting, statistics, and confidence intervals in the graph panel.
    """
    def __init__(
        self,
        context,
        confidence_service,
        graph_panel,
        update_statistics_callback: Callable[[], None],
        update_gof_callback: Callable[[], None]
    ):
        """
        Args:
            context: AppContext with shared data
            confidence_service: Service for confidence interval computations
            graph_panel: Visualization panel hosting graph tabs and controls.
            update_statistics_callback: function to trigger statistics table update
            update_gof_callback: function to trigger goodness-of-fit tests
        """
        self.context = context
        self.panel = graph_panel
        self.confidence_service = confidence_service
        self.update_statistics_callback = update_statistics_callback
        self.update_gof_callback = update_gof_callback

    def set_data(self, series: pd.Series) -> None:
        """
        Set data and refresh everything.
        """
        self.panel.data = series
        if series is not None and not series.empty:
            self.plot_all()

    def plot_all(self) -> None:
        """
        Redraw graphs and update both stats and GOF tests.
        """
        self.panel.refresh_all()
        self.update_statistics_callback()
        self.update_gof_callback()

    def on_distribution_changed(self) -> None:
        """
        Called when distribution is changed. Redraws and reruns GOF.
        """
        if not self._valid():
            return
        self.panel.refresh_all()
        self.update_gof_callback()

    def on_bins_changed(self) -> None:
        """
        Called when number of bins is changed. Full redraw and recompute.
        """
        if self._valid():
            self.plot_all()

    def on_alpha_changed(self) -> None:
        """
        Called when confidence level is changed.
        """
        if self._valid():
            self.panel.refresh_all()

    def on_kde_toggled(self) -> None:
        """
        Called when KDE checkbox toggled. Redraw only.
        """
        if self._valid():
            self.panel.refresh_all()

    def compute_cdf_with_ci(self, data: pd.Series, dist, confidence_level: float) -> tuple:
        """
        Compute confidence intervals for CDF using provided service.
        """
        return self.confidence_service.cdf_variance_ci(data, dist, confidence_level)

    def _valid(self) -> bool:
        """
        Check if current data is usable.
        """
        return (
            self.context.data_model is not None and
            isinstance(self.context.data_model.series, pd.Series) and
            not self.context.data_model.series.empty
        )