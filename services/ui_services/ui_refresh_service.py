class UIRefreshService:
    """
    Service for refreshing all UI components after data changes.
    """

    @staticmethod
    def refresh_all(window, series):
        """
        Refresh graphs, statistics, and test results in the UI after data update.

        :param window: main application window
        :param series: current data series to visualize
        """
        if series is None or series.isna().sum() > 0:
            # Clear if missing
            window.graph_panel.clear()
            window.graph_panel.data = None
            window.stat_controller.clear()
            window.gof_tab.clear_tests()
        else:
            # Update model bins before plotting
            if window.data_model:
                window.data_model.update_bins(window.graph_panel.bins_spinbox.value())
                
            # Update visualizations and stats
            window.graph_controller.set_data(series)
            window.stat_controller.update_statistics_table()
            window.gof_tab.evaluate_tests()

        # Always update UI state and navigation
        window.state_controller.update_state_for_data(series)
        window.state_controller.update_transformation_label()
        window.state_controller.update_navigation_buttons()
        window.original_button.setEnabled(True)
