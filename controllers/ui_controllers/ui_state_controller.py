class UIStateController:
    """
    Controller responsible for enabling/disabling UI elements based on data state.
    """

    def __init__(self, window):
        """
        Args:
            window (QWidget): Reference to the main application window
        """
        self.window = window

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
        """
        Enables/disables transformation-related buttons.
        """
        self.window.standardize_button.setEnabled(enabled)
        self.window.log_button.setEnabled(enabled)
        self.window.shift_spinbox.setEnabled(enabled)
        self.window.shift_button.setEnabled(enabled)

    def _update_anomaly_buttons(self, enabled: bool):
        """
        Enables/disables anomaly detection-related buttons.
        """
        self.window.normal_anomaly_button.setEnabled(enabled)
        self.window.asymmetry_anomaly_button.setEnabled(enabled)
        self.window.confidence_anomaly_button.setEnabled(enabled)
        self.window.anomaly_gamma_spinbox.setEnabled(enabled)

    def _update_missing_buttons(self, enabled: bool):
        """
        Enables/disables buttons related to handling missing values.
        """
        self.window.impute_mean_button.setEnabled(enabled)
        self.window.impute_median_button.setEnabled(enabled)
        self.window.interpolate_linear_button.setEnabled(enabled)
        self.window.drop_missing_button.setEnabled(enabled)

    def update_transformation_label(self):
        """
        Updates the UI label indicating the current transformation chain/state.
        """
        text = self.window.data_model.current_transformation if self.window.data_model else "Original"
        self.window.transformation_label.setText(f"Current state: {text}")

    def update_navigation_buttons(self):
        """
        Enables the 'Original' button if transformation history or anomaly filtering exists.
        """
        model = self.window.data_model
        has_history = model and len(model.history) > 0
        was_anomaly_removed = getattr(model, 'anomalies_removed', False)
        self.window.original_button.setEnabled(has_history or was_anomaly_removed)