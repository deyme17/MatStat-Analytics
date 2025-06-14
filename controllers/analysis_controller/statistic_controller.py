class StatisticController:
    """
    Controller for managing the display of statistical characteristics in the UI.
    """
    def __init__(self, context, statistic_service, stats_renderer, stat_tab, 
                 precision_spinbox, confidence_spinbox):
        """
        Args:
            context (AppContext): Application context container
            statistic_service: Service for statistics handling
            stats_renderer: UI service for statistics visualization
            stat_tab (StatisticTab): Reference to the statistics display tab widget
            precision_spinbox: SpinBox control for precision configuration
            confidence_spinbox: SpinBox control for confidence level selection
        """
        self.context = context
        self.statistic_service = statistic_service
        self.stats_renderer = stats_renderer
        self.stat_tab = stat_tab                      
        self.precision_spinbox = precision_spinbox        
        self.confidence_spinbox = confidence_spinbox        

    def update_statistics_table(self):
        """
        Recalculate statistics and update the UI statistics table.
        """
        model = self.context.data_model
        if model is None or model.series.empty:
            return
        
        bins = self.context.bins_spinbox.value()
        model.update_bins(bins)

        confidence = self.confidence_spinbox.value()
        precision = self.precision_spinbox.value()

        # calc stats
        stats_data = self.statistic_service.get_characteristics(model.hist)
        ci_data = self.statistic_service.compute_intervals(model.series, confidence_level=confidence, precision=precision)

        # visualize table
        self.stats_renderer.render_stats_table(
            self.stat_tab.conf_table,
            stats_data.to_dict(),
            ci_data.to_dict(),
            precision=precision
        )

    def clear(self):
        """
        Clear the contents of the statistics table.
        """
        self.stat_tab.conf_table.clearContents()
        self.stat_tab.conf_table.setRowCount(0)