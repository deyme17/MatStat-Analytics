class UIRefreshService:
    @staticmethod
    def refresh_all(window, series):
        if series is None or series.isna().sum() > 0:
            # Clear if missing
            window.graph_panel.clear()
            window.graph_panel.data = None
            window.stat_controller.clear()
            window.gof_tab.clear_tests()
        else:
            if window.data_model:
                window.data_model.update_bins(window.graph_panel.bins_spinbox.value())
                
            window.graph_controller.set_data(series)
            window.stat_controller.update_statistics_table()
            window.gof_tab.evaluate_tests()

        # Always update state
        window.state_controller.update_state_for_data(series)
        window.state_controller.update_transformation_label()
        window.state_controller.update_navigation_buttons()
        window.original_button.setEnabled(True)
