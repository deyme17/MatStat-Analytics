class StatisticController:
    """
    Controller for managing the display of statistical characteristics in the UI.
    """

    def __init__(self, window, statistic_service):
        """
        Args:
            window (QWidget): Reference to the main application window
            statistic_service: Service for statistics handling
        """
        self.window = window
        self.statistic_service = statistic_service

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

        self.statistic_service.update_table(
            self.window.stat_tab.conf_table,
            model.hist,
            model.series,
            precision=self.window.precision_spinbox.value(),
            confidence_level=confidence
        )

    def clear(self):
        """
        Clear the contents of the statistics table.
        """
        self.window.stat_tab.conf_table.clearContents()
        self.window.stat_tab.conf_table.setRowCount(0)
