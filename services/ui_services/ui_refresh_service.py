class UIRefreshService:
    """
    Service for refreshing all UI components after data changes.
    
    Responsibilities:
    - Clears or updates UI elements based on data state
    - Updates model bins when data is valid
    - Refreshes visualizations and statistics
    - Maintains application state consistency
    """

    def __init__(self, window):
        """
        Initialize the service with the main application window.
        
        :param window: main application window containing all UI components
        """
        self.window = window

    def refresh(self, series):
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
        self.window.graph_panel.clear()
        self.window.graph_panel.data = None
        self.window.stat_controller.clear()
        self.window.gof_tab.clear_panels()

    def _update_model_bins(self):
        """Update the data model with current bin count if model exists."""
        if self.window.data_model:
            self.window.data_model.update_bins(self.window.graph_panel.bins_spinbox.value())

    def _update_visuals(self, series):
        """Update all visual elements with new data."""
        self.window.graph_controller.set_data(series)
        self.window.stat_controller.update_statistics_table()
        self.window.gof_tab.evaluate_tests()

    def _update_state(self, series):
        """Update application state and navigation controls."""
        self.window.state_controller.update_state_for_data(series)
        self.window.state_controller.update_transformation_label()
        self.window.state_controller.update_navigation_buttons()
        self.window.original_button.setEnabled(True)