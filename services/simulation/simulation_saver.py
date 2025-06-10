import numpy as np
import pandas as pd
from models.data_model import DataModel
from utils.def_bins import get_default_bin_count


class DataSaver:
    def __init__(self, window):
        """
        :param window: Main window instance for accessing version_manager and showing messages
        """
        self.window = window
        self.simulation_counter = {}
        
    def save_data(self, dist_name: str, data: np.ndarray):
        """
        Save simulated data as a new dataset in the data history manager.
        
        :param dist_name: name of the distribution
        :param data: simulated data array
        """
        dataset_label = self._create_data_label(dist_name)
        series = pd.Series(data)
        
        # data
        optimal_bins = get_default_bin_count(series)
        data_model = DataModel(series, bins=optimal_bins, label=dataset_label)

        # Add to version manager and update window state
        self.window.version_manager.add_dataset(dataset_label, data_model)
        self.window.data_model = data_model
        self.window.state_controller.handle_post_load_state(series)
        
        # success message
        self.window.show_info_message(
            "Data Saved", 
            f"Simulated data saved as '{dataset_label}' with {len(data)} samples."
        )

    def _create_data_label(self, dist_name):
        """Creates a label for newly-generated data"""
        if dist_name not in self.simulation_counter:
            self.simulation_counter[dist_name] = 0
        
        self.simulation_counter[dist_name] += 1
        counter = self.simulation_counter[dist_name]
        
        return f"{dist_name}Simulation{counter}"