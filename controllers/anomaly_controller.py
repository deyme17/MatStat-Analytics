from utils.data_func import detect_anomalies, detect_normal_anomalies
from views.plot_graphs import plot_graphs
import numpy as np

class AnomalyController:
    """Controller for handling anomaly detection and removal."""
    
    def __init__(self, window):
        self.window = window

    def remove_normal_anomalies(self):
        """Remove anomalies using normal distribution."""
        if self.window.data is not None:
            result = detect_normal_anomalies(self.window.data)
            self._process_anomalies(result)

    def remove_anomalies(self):
        """Remove anomalies using asymmetry coefficient."""
        if self.window.data is not None:
            result = detect_anomalies(self.window.data)
            self._process_anomalies(result)

    def _process_anomalies(self, result):
        """Process detected anomalies and update data."""
        anomalies = result['anomalies']
        if len(anomalies) > 0:
            # store orig data
            if not hasattr(self.window, 'original_data_backup'):
                self.window.original_data_backup = self.window.data_processor.get_original_data()
            
            self.window.ui_controller.anomalies_removed = True
            
            # remove anomalies
            filtered_data = self.window.data.drop(anomalies)
            
            # update data
            self.window.data = filtered_data
            
            # update data in data_processor
            current_index = self.window.data_processor.current_index
            filename = self.window.data_processor.get_data_description()
            self.window.data_processor.data_history[current_index] = (filename, filtered_data.copy())
            
            # update UI
            self.window.ui_controller.update_navigation_buttons()
            plot_graphs(self.window)
            
            # disable anomaly detection buttons
            self.window.normal_anomaly_button.setEnabled(False)
            self.window.asymmetry_anomaly_button.setEnabled(False)
            
            self.window.show_info_message("Anomalies Removed", f"Removed {len(anomalies)} anomalous data points.")
        else:
            self.window.show_info_message("No Anomalies", "No anomalies were detected in the current dataset.")