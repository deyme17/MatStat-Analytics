class StatisticController:
    """
    Controller for managing the display of statistical characteristics in the UI.
    """

    def __init__(self, window, statistic_service, stats_renderer):
        """
        Args:
            window (QWidget): Reference to the main application window
            statistic_service: Service for statistics handling
            stats_renderer: UI service for statistics visualization
        """
        self.window = window
        self.statistic_service = statistic_service
        self.stats_renderer = stats_renderer

    def update_statistics_table(self):
        """
        Recalculate statistics and update the UI statistics table.
        """
        model = self.window.data_model
        if model is None or model.series.empty:
            return
        
        bins = self.window.graph_panel.bins_spinbox.value()
        model.update_bins(bins)

        confidence = self.window.graph_panel.confidence_spinbox.value()
        precision = self.window.precision_spinbox.value()

        # calc stats
        stats_data = self.statistic_service.get_characteristics(model.hist)
        ci_data = self.statistic_service.compute_intervals(model.series, confidence_level=confidence, precision=precision)

        # visualize table
        self.stats_renderer.render_stats_table(
            self.window.stat_tab.conf_table,
            stats_data.to_dict(),
            ci_data.to_dict(),
            precision=precision
        )

    def clear(self):
        """
        Clear the contents of the statistics table.
        """
        self.window.stat_tab.conf_table.clearContents()
        self.window.stat_tab.conf_table.setRowCount(0)