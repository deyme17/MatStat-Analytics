from typing import Callable, Optional
from callbacks.ui_graph_callbacks import GraphPanelCallbacks
import pandas as pd

class GraphController:
    """
    Controller for coordinating plotting, statistics, and confidence intervals in the graph panel.
    """
    def __init__(
        self,
        context,
        confidence_service,
        graph_control: Optional[GraphPanelCallbacks] = None,
        update_statistics_callback: Optional[Callable[[], None]] = None,
        update_gof_callback: Optional[Callable[[], None]] = None
    ):
        """
        Args:
            context: AppContext with shared data
            confidence_service: Service for confidence interval computations
            graph_control: Container of graph_panel control callbacks
            update_statistics_callback: function to trigger statistics table update
            update_gof_callback: function to trigger goodness-of-fit tests
        """
        self.context = context
        self.panel = graph_control
        self.confidence_service = confidence_service
        self.update_statistics_callback = update_statistics_callback
        self.update_gof_callback = update_gof_callback

    def set_data(self, series: pd.Series) -> None:
        """
        Set data and refresh everything.
        """
        self.check_all_callbacks()
        self.panel.set_data(series)
        if series is not None and not series.empty:
            self.plot_all()

    def plot_all(self) -> None:
        """
        Redraw graphs and update both stats and GOF tests.
        """
        self.check_all_callbacks()
        self.panel.refresh_all()
        self.update_statistics_callback()
        self.update_gof_callback()

    def on_distribution_changed(self) -> None:
        """
        Called when distribution is changed. Redraws and reruns GOF.
        """
        self.check_all_callbacks()
        if self._valid():
            self.panel.refresh_all()
            self.update_gof_callback()

    def on_bins_changed(self) -> None:
        """
        Called when number of bins is changed. Full redraw and recompute.
        """
        self.check_all_callbacks()
        if self._valid():
            self.plot_all()

    def on_alpha_changed(self) -> None:
        """
        Called when confidence level is changed.
        """
        self.check_all_callbacks()
        if self._valid():
            self.plot_all()

    def on_kde_toggled(self) -> None:
        """
        Called when KDE checkbox toggled. Redraw only.
        """
        self.check_all_callbacks()
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
    
    def connect_callbacks(self, graph_control: GraphPanelCallbacks,
                                update_statistics_callback: Callable[[], None],
                                update_gof_callback: Callable[[], None]) -> None:
        self.panel = graph_control
        self.update_statistics_callback = update_statistics_callback
        self.update_gof_callback = update_gof_callback

    def check_all_callbacks(self) -> None:
        if not (self.panel and self.update_statistics_callback and self.update_gof_callback):
            raise RuntimeError("Not all callbacks provided for GraphController")