class MissingDataController:
    """
    Controller for handling missing data operations.
    """

    def __init__(self, window, missing_service):
        """
        Args:
            window (QWidget): Reference to the main application window
            missing_service: Service layer for missing data operations
        """
        self.window = window
        self.missinf_service = missing_service
        self.data = None

    def update_data_reference(self, data):
        """
        Set new working data and refresh UI information.

        :param data: pandas Series
        """
        self.data = data
        self.update_missing_values_info()
        self.window.state_controller.update_state_for_data(data)

    def update_missing_values_info(self):
        """
        Update labels showing total and percentage of missing values.
        """
        if self.data is not None:
            info = self.missing_service.detect_missing(self.data)
            self.window.missing_count_label.setText(f"Total Missing: {info['total_missing']}")
            self.window.missing_percentage_label.setText(f"Missing Percentage: {info['missing_percentage']:.2f}%")

    def _update_after_imputation(self, new_series, label: str, message: str):
        """
        Create new version of the data after missing value handling and refresh UI.

        :param new_series: modified series after imputation
        :param label: version label
        :param message: message to display to the user
        """
        new_model = self.window.data_model.add_version(new_series, label)
        self.window.data_model = new_model
        self.data = new_model.series

        self.window.version_manager.update_current_data(new_model)
        self.window.refresher.refresh_all(self.window, new_series)
        self.update_missing_values_info()
        self.window.show_info_message("Success", message)

    def impute_with_mean(self):
        """
        Replace missing values with the mean of the series.
        """
        if self.data is not None:
            new_series = self.missing_service.replace_missing_with_mean(self.data)
            self._update_after_imputation(new_series, "Mean Imputed", "Missing values replaced with mean successfully.")

    def impute_with_median(self):
        """
        Replace missing values with the median of the series.
        """
        if self.data is not None:
            new_series = self.missing_service.replace_missing_with_median(self.data)
            self._update_after_imputation(new_series, "Median Imputed", "Missing values replaced with median successfully.")

    def interpolate_missing(self, method: str):
        """
        Interpolate missing values using the specified method.

        :param method: interpolation method ('linear', 'quadratic', 'cubic')
        """
        if self.data is not None:
            new_series = self.missing_service.interpolate_missing(self.data, method)
            self._update_after_imputation(new_series, f"Interpolated ({method})", f"Missing values interpolated ({method}) successfully.")

    def drop_missing_values(self):
        """
        Drop all rows containing missing values from the series.
        """
        if self.data is not None:
            original_len = len(self.data)
            new_series = self.missing_service.drop_missing(self.data)
            dropped = original_len - len(new_series)
            self._update_after_imputation(new_series, "Dropped NA", f"Dropped {dropped} rows with missing values.")