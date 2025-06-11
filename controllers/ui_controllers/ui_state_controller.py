import pandas as pd

class UIStateController:
    """
    Controller responsible for enabling/disabling UI elements based on data state.
    """

    def __init__(self, window, missing_service):
        """
        Args:
            window (QWidget): Reference to the main application window
            missing_service: Service to handle anomilies
        """
        self.window = window
        self.missing_service = missing_service

    def handle_post_load_state(self, data: pd.Series):
        """
        Centralized method to be called after loading data.
        Updates UI state and handles missing values and control logic.
        """
        missing_info = self.missing_service.detect_missing(data)
        has_missing = missing_info['total_missing'] > 0

        # Enable fixed elements
        self.window.graph_panel.bins_spinbox.setEnabled(True)
        self.window.data_version_combo.setEnabled(True)

        # Update controls
        self.update_state_for_data(data)

        # Update other controllers
        self.window.data_version_controller.update_data_versions()
        self.window.missing_controller.update_data_reference(data)

        # Set bin count
        bin_count = self.window.data_model.bins
        self.window.graph_panel.bins_spinbox.setValue(bin_count)

        if has_missing:
            self.window.show_info_message(
                "Missing Values Detected",
                f"Found {missing_info['total_missing']} missing values "
                f"({missing_info['missing_percentage']:.2f}%).\n"
                "Please handle missing values before performing data operations."
            )
            self.window.graph_panel.clear()
            self.window.graph_panel.data = None
            self.window.gof_tab.clear_tests()
            self.window.stat_controller.clear()
        else:
            self.window.refresher.refresh(self.window.data_model.series)

    def update_state_for_data(self, data):
        """
        Updates the enabled state of all major UI controls based on the data.
        If missing values are present, disables transformations and anomaly controls.

        :param data: The current pandas Series to check for missing values.
        """
        has_missing = data.isna().sum() > 0 if hasattr(data, 'isna') else False

        self.window.data_tab.process_controls.setEnabled(not has_missing)
        self.window.data_tab.anomaly_detection.setEnabled(not has_missing)
        self.window.data_tab.missing_data.setEnabled(True)

        self._update_transform_buttons(not has_missing)
        self._update_anomaly_buttons(not has_missing)
        self._update_missing_buttons(has_missing)

        self.update_transformation_label()
        self.update_navigation_buttons()

    def _update_transform_buttons(self, enabled: bool):
        self.window.standardize_button.setEnabled(enabled)
        self.window.log_button.setEnabled(enabled)
        self.window.shift_spinbox.setEnabled(enabled)
        self.window.shift_button.setEnabled(enabled)

    def _update_anomaly_buttons(self, enabled: bool):
        self.window.normal_anomaly_button.setEnabled(enabled)
        self.window.asymmetry_anomaly_button.setEnabled(enabled)
        self.window.confidence_anomaly_button.setEnabled(enabled)
        self.window.anomaly_gamma_spinbox.setEnabled(enabled)

    def _update_missing_buttons(self, enabled: bool):
        self.window.impute_mean_button.setEnabled(enabled)
        self.window.impute_median_button.setEnabled(enabled)
        self.window.interpolate_linear_button.setEnabled(enabled)
        self.window.drop_missing_button.setEnabled(enabled)

    def update_transformation_label(self):
        text = self.window.data_model.current_transformation if self.window.data_model else "Original"
        self.window.transformation_label.setText(f"Current state: {text}")

    def update_navigation_buttons(self):
        model = self.window.data_model
        has_history = model and len(model.history) > 0
        was_anomaly_removed = getattr(model, 'anomalies_removed', False)
        self.window.original_button.setEnabled(has_history or was_anomaly_removed)
