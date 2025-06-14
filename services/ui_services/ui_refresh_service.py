from typing import Callable, Optional
import pandas as pd


class UIRefreshService:
    """
    Service for refreshing all UI components after data changes.
    
    Uses callbacks to decouple from specific UI components.
    """
    def __init__(
        self,
        # Clear operations
        clear_graph_callback: Callable[[], None],
        clear_stats_callback: Callable[[], None],
        clear_gof_callback: Callable[[], None],
        
        # Update operations
        set_graph_data_callback: Callable[[Optional[pd.Series]], None],
        update_stats_callback: Callable[[], None],
        evaluate_gof_callback: Callable[[], None],
        
        # State operations
        update_state_callback: Callable[[pd.Series], None],
        update_transformation_label_callback: Callable[[], None],
        update_navigation_buttons_callback: Callable[[], None],
        enable_original_button_callback: Callable[[bool], None],
        
        # Model operations
        get_bins_count_callback: Callable[[], int],
        update_model_bins_callback: Optional[Callable[[int], None]] = None
    ):
        """
        Args:
            clear_graph_callback: Clears graph visualization
            clear_stats_callback: Resets statistics display
            clear_gof_callback: Clears goodness-of-fit tests
            
            set_graph_data_callback: Updates graph with new data series
            update_stats_callback: Refreshes statistics calculations
            evaluate_gof_callback: Re-runs goodness-of-fit tests
            
            update_state_callback: Updates application state for new data
            update_transformation_label_callback: Refreshes transform status
            update_navigation_buttons_callback: Updates button states
            enable_original_button_callback: Toggles 'Original' button
            
            get_bins_count_callback: Retrieves current bin count
            update_model_bins_callback: Updates model's bin count (optional)
        """
        # Clear callbacks
        self.clear_graph = clear_graph_callback
        self.clear_stats = clear_stats_callback
        self.clear_gof = clear_gof_callback
        
        # Update callbacks
        self.set_graph_data = set_graph_data_callback
        self.update_stats = update_stats_callback
        self.evaluate_gof = evaluate_gof_callback
        
        # State callbacks
        self.update_state = update_state_callback
        self.update_transformation_label = update_transformation_label_callback
        self.update_navigation_buttons = update_navigation_buttons_callback
        self.enable_original_button = enable_original_button_callback
        
        # Model callbacks
        self.get_bins_count = get_bins_count_callback
        self.update_model_bins = update_model_bins_callback

    def refresh(self, series: pd.Series):
        """
        Main refresh method that updates all UI components based on data state.
        
        :param series: current data series to visualize (pandas Series)
        """
        if series is None or series.isna().sum() > 0:
            self.clear_ui()
        else:
            self._update_model_bins()
            self._update_visuals(series)

        self._update_state(series)

    def clear_ui(self):
        """Clear all UI elements when data is missing or invalid."""
        self.clear_graph()
        self.set_graph_data(None)
        self.clear_stats()
        self.clear_gof()

    def _update_model_bins(self):
        """Update the data model with current bin count if model exists."""
        if self.update_model_bins:
            bins_count = self.get_bins_count()
            self.update_model_bins(bins_count)

    def _update_visuals(self, series: pd.Series):
        """Update all visual elements with new data."""
        self.set_graph_data(series)
        self.update_stats()
        self.evaluate_gof()

    def _update_state(self, series: pd.Series):
        """Update application state and navigation controls."""
        self.update_state(series)
        self.update_transformation_label()
        self.update_navigation_buttons()
        self.enable_original_button(True)