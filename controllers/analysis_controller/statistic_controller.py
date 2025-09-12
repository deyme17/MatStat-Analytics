from typing import Callable, Optional
from services.ui_services.renderers.table_renderers.table_renderer import TableRenderer


class StatisticController:
    """
    Controller for managing the display of statistical characteristics in the UI.
    """
    def __init__(self, context, statistic_service,
                 stats_renderer: Optional[TableRenderer] = None,
                 var_renderer: Optional[TableRenderer] = None,
                 get_bins_value: Optional[Callable[[], int]] = None, 
                 get_precision_value: Optional[Callable[[], int]] = None,
                 get_confidence_value: Optional[Callable[[], float]] = None
                 ):
        """
        Args:
            context (AppContext): Application context container
            statistic_service: Service for statistics handling
            stats_renderer (StatsRenderer): Responsible for drawing statistics in table
            var_renderer (VarSerRenderer): Responsible for drawing variation series in table
            get_bins_value: Function for getting bin count configuration
            get_precision_value: Function for getting precision configuration
            get_confidence_value: Function for getting confidence level selection
        """
        self.context = context
        self.statistic_service = statistic_service
        self.stats_renderer = stats_renderer
        self.var_renderer = var_renderer
        self.get_bins_value = get_bins_value             
        self.get_precision_value = get_precision_value        
        self.get_confidence_value = get_confidence_value    

    def update_tables(self) -> None:
        """Updates all the UI tables"""
        self.check_ui_connected()
        model = self.context.data_model
        if model is None or model.series.empty:
            return
        
        bins = self.get_bins_value()
        model.update_bins(bins)
        
        self._update_statistic_table(model)
        self._update_var_series_table(model)

    def _update_statistic_table(self, model) -> None:
        """
        Recalculate statistics and update the UI tables.
        Args:
            model: DataModel
        """
        stats_data = self.statistic_service.get_characteristics(model.hist)
        ci_data = self.statistic_service.compute_intervals(
            model.series,
            confidence_level=self.get_confidence_value(),
            precision=self.get_precision_value()
        )
        self.stats_renderer.render(
            stats_data.to_dict(),
            ci_data.to_dict(),
            precision=self.get_precision_value()
        )

    def _update_var_series_table(self, model) -> None:
        """
        Recalculate variation series and update the UI tables.
        Args:
            model: DataModel
        """
        data = self.statistic_service.get_var_series(model.hist)
        self.var_renderer.render(data.to_dict())

    def clear_tables(self) -> None:
        """
        Clear the contents of tables via renderer.
        """
        self.check_ui_connected()
        self.stats_renderer._setup_headers()
        self.var_renderer._setup_headers()

    def connect_ui(self, stats_renderer: TableRenderer, var_renderer: TableRenderer, get_bins_value: Callable[[], int], 
                get_precision_value: Callable[[], int], get_confidence_value: Callable[[], float]) -> None:
        self.stats_renderer = stats_renderer
        self.var_renderer = var_renderer
        self.get_bins_value = get_bins_value             
        self.get_precision_value = get_precision_value        
        self.get_confidence_value = get_confidence_value

    def check_ui_connected(self) -> None:
        if not (self.stats_renderer and self.var_renderer and self.get_bins_value 
                and self.get_precision_value and self.get_confidence_value):
            raise RuntimeError("Not all ui functions&callbacks connected to StatisticController")