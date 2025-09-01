from callbacks import UIClearCallbacks, UIUpdateCallbacks, UIModelCallbacks, UIStateCallbacks
import pandas as pd


class UIRefreshService:
    """
    Service for refreshing all UI components after data changes.
    Uses grouped callbacks to decouple from specific UI components.
    """
    def __init__(
        self,
        clear: UIClearCallbacks,
        update: UIUpdateCallbacks,
        state: UIStateCallbacks,
        model: UIModelCallbacks
    ):
        """
        Args:
            clear: Group of callbacks for clearing graph/stat/GOF UI
            update: Group of callbacks for updating UI elements
            state: Group of callbacks for updating app state/labels/buttons
            model: Group of callbacks for accessing/updating the data model
        """
        self.clear = clear
        self.update = update
        self.state = state
        self.model = model

    def refresh(self, series: pd.Series) -> None:
        """
        Main refresh method that updates all UI components based on data state.
        Args:
            series: current data series to visualize (pandas Series)
        """
        if series is None or series.isna().sum() > 0:
            self.clear_ui()
        else:
            self._update_model_bins()
            self._update_visuals(series)

        self._update_state(series)

    def clear_ui(self) -> None:
        """Clear all UI elements when data is missing or invalid."""
        self.clear.clear_graph()
        self.update.set_graph_data(None)
        self.clear.clear_stats()
        self.clear.clear_gof()

    def _update_model_bins(self) -> None:
        """Update the data model with current bin count if model exists."""
        if self.model.update_model_bins:
            bins_count = self.model.get_bins_count()
            self.model.update_model_bins(bins_count)

    def _update_visuals(self, series: pd.Series) -> None:
        """Update all visual elements with new data."""
        self.update.set_graph_data(series)
        self.update.update_stats()
        self.update.evaluate_gof()

    def _update_state(self, series: pd.Series) -> None:
        """Update application state and navigation controls."""
        self.state.update_state(series)
        self.state.update_transformation_label()
        self.state.update_navigation_buttons()
        self.state.enable_original_button(True)