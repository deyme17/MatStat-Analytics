from models import StatisticsCalculator
from utils import EventBus, EventType, Event, AppContext


class StatisticsController:
    """
    Controller for managing statistical calculations and broadcasting standard results.
    """
    def __init__(self, context: AppContext, stat_calculator: StatisticsCalculator):
        """
        Args:
            context: Shared application context (with event_bus).
            stat_calculator: Class for statistics handling.
        """
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.stat_calculator: StatisticsCalculator = stat_calculator

        self.bins: int | None = None
        self.precision: int = 2
        self.confidence: float = 0.95

        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        """Subscribe to data state changes and parameter input events."""
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_TRANSFORMED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.COLUMN_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_changed)
        self.event_bus.subscribe(EventType.MISSING_VALUES_DETECTED, self._on_missings)
        self.event_bus.subscribe(EventType.BINS_CHANGED, self._on_bins_changed)
        self.event_bus.subscribe(EventType.CONFIDENCE_CHANGED, self._on_confidence_changed)
        self.event_bus.subscribe(EventType.PRECISION_CHANGED, self._on_precision_changed)

    def _on_bins_changed(self, event: Event) -> None:
        if isinstance(event.data, int):
            self.bins = event.data
            self.recalculate()

    def _on_confidence_changed(self, event: Event) -> None:
        if isinstance(event.data, (float, int)):
            self.confidence = float(event.data)
            self.recalculate()

    def _on_precision_changed(self, event: Event) -> None:
        if isinstance(event.data, int):
            self.precision = event.data
            self.recalculate()

    def _on_data_changed(self, event: Event) -> None:
        self.recalculate()

    def _on_missings(self, event: Event) -> None:
        self.event_bus.emit_type(EventType.STATS_CLEARED)

    def recalculate(self) -> None:
        """Recalculate statistics and emit calculated results via EventBus."""
        model = self.context.data_model
        if model is None or model.series.empty:
            return

        if self.bins is not None:
            model.update_bins(self.bins)
        
        stats_data = self.stat_calculator.get_characteristics(model.hist)
        ci_data = self.stat_calculator.compute_intervals(
            model.series,
            confidence_level=self.confidence,
            precision=self.precision
        )
        var_series_data = self.stat_calculator.get_var_series(model.hist)
        multi_var_data = self.stat_calculator.get_multi_var_stats(model.dataframe)

        self.event_bus.emit_type(EventType.STATS_UPDATED, {
            "stats": stats_data.to_dict(),
            "ci": ci_data.to_dict(),
            "var_series": var_series_data.to_dict(),
            "multi_var": multi_var_data,
            "precision": self.precision
        })