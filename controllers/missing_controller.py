from services.missing_service import MissingService

class MissingDataController:
    def __init__(self, window):
        self.window = window
        self.data = None

    def update_data_reference(self, data):
        self.data = data
        self.update_missing_values_info()
        self.window.state_controller.update_state_for_data(data)

    def update_missing_values_info(self):
        if self.data is not None:
            info = MissingService.detect_missing(self.data)
            self.window.missing_count_label.setText(f"Total Missing: {info['total_missing']}")
            self.window.missing_percentage_label.setText(f"Missing Percentage: {info['missing_percentage']:.2f}%")

    def _update_after_imputation(self, new_data, message):
        if self.data is not None:
            self.window.data = new_data
            self.data = new_data
            self.window.version_manager.update_current_data(new_data)

            if self.window.transform_manager.transformed_data is not None:
                self.window.transform_manager.transformed_data = new_data.copy()

            self.window.graph_controller.set_data(new_data)
            self.window.stat_controller.update_statistics_table()
            self.update_missing_values_info()
            self.window.state_controller.update_state_for_data(new_data)

            self.window.original_button.setEnabled(True)
            self.window.show_info_message("Success", message)

    def impute_with_mean(self):
        if self.data is not None:
            new_data = MissingService.replace_missing_with_mean(self.data)
            self._update_after_imputation(new_data, "Missing values replaced with mean successfully.")

    def impute_with_median(self):
        if self.data is not None:
            new_data = MissingService.replace_missing_with_median(self.data)
            self._update_after_imputation(new_data, "Missing values replaced with median successfully.")

    def interpolate_missing(self, method):
        if self.data is not None:
            new_data = MissingService.interpolate_missing(self.data, method)
            self._update_after_imputation(new_data, f"Missing values interpolated ({method}) successfully.")

    def drop_missing_values(self):
        if self.data is not None:
            original_len = len(self.data)
            new_data = MissingService.drop_missing(self.data)
            dropped = original_len - len(new_data)
            self._update_after_imputation(new_data, f"Dropped {dropped} rows with missing values.")