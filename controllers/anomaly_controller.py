from services.anomaly_service import AnomalyService

class AnomalyController:
    def __init__(self, window):
        self.window = window

    def remove_normal_anomalies(self):
        self._remove_anomalies(AnomalyService.detect_normal_anomalies)

    def remove_asymmetry_anomalies(self):
        self._remove_anomalies(AnomalyService.detect_asymmetry_anomalies)

    def remove_conf_anomalies(self):
        gamma = self.window.anomaly_gamma_spinbox.value()
        self._remove_anomalies(lambda data: AnomalyService.detect_conf_anomalies(data, gamma))

    def _remove_anomalies(self, detection_func):
        data = self.window.data
        if data is None:
            return

        data = data.reset_index(drop=True)
        if data.isna().sum() > 0:
            self.window.show_error_message("Missing Values Error", "Please handle missing values first.")
            return

        result = detection_func(data)
        anomalies = result["anomalies"]
        if len(anomalies) == 0:
            self.window.show_info_message("No Anomalies", "No anomalies detected.")
            return

        cleaned = data.drop(anomalies)
        self.window.data = cleaned
        self.window.graph_controller.set_data(cleaned)
        self.window.stat_controller.update_statistics_table()

        self.window.version_manager.update_current_data(cleaned)
        self.window.anomalies_removed = True
        self.window.state_controller.update_state_for_data(cleaned)

        self.window.show_info_message(
            "Anomalies Removed",
            f"Removed {len(anomalies)} anomalies.\n"
            f"Lower: {result['lower_limit']:.4f}, Upper: {result['upper_limit']:.4f}"
        )