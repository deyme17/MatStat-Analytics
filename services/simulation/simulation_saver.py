import numpy as np
import pandas as pd
from typing import Callable
from models.data_model import DataModel
from utils.def_bins import get_default_bin_count


class DataSaver:
    def __init__(self, context, on_save: Callable[[pd.Series], None]):
        """
        Args:
            context (AppContext): Application context container
            on_save: Callback to applying data saving
        """
        self.context = context
        self.simulation_counter = {}
        self.on_save = on_save
        
    def save_data(self, dist_name: str, data: np.ndarray) -> None:
        """
        Save simulated data as a new dataset in the data history manager.
        Args:
            dist_name: name of the distribution
            data: simulated data array (1D or 2D)
        """
        dataset_label = self._create_data_label(dist_name)
        
        if data.ndim == 1:
            df = pd.DataFrame(data, columns=['data'])
        elif data.ndim == 2:
            df = pd.DataFrame(data, columns=[f"col{i+1}" for i in range(data.shape[1])])
        else:
            raise ValueError(f"Unsupported data dimensionality: {data.ndim}D")
        
        optimal_bins = get_default_bin_count(df)
        data_model = DataModel(df, bins=optimal_bins, label=dataset_label)

        self.context.version_manager.add_dataset(dataset_label, data_model)
        self.context.data_model = data_model

        if self.on_save:
            self.on_save(data_model.series)
        
        self.context.messanger.show_info(
            "Data Saved", 
            f"Simulated data saved as '{dataset_label}' with {len(data)} samples."
        )

    def _create_data_label(self, dist_name) -> str:
        """Creates a label for newly-generated data"""
        if dist_name not in self.simulation_counter:
            self.simulation_counter[dist_name] = 0
        
        self.simulation_counter[dist_name] += 1
        counter = self.simulation_counter[dist_name]
        
        return f"{dist_name}Simulation{counter}"