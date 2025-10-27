import numpy as np
import pandas as pd
from models.data_model import DataModel
from utils.def_bins import get_default_bin_count


class DataSaver:
    def __init__(self):
        self.counter = {}
        
    def save_data(self, dist_name: str, data: np.ndarray, type_: str = "Simulation") -> DataModel:
        """
        Save np.ndarray data as a new dataset.
        Args:
            dist_name: name of the distribution
            data: simulated data array (1D or 2D)
            type_: type of data (e.g. "Simulation", "Exported")
        Returns:
            data saved as DataModel
        """
        dataset_label = self._create_data_label(dist_name, type_, str(data.shape[1]))
        
        if data.ndim == 1:
            df = pd.DataFrame(data, columns=['value'])
        elif data.ndim == 2:
            df = pd.DataFrame(data, columns=[f"col{i+1}" for i in range(data.shape[1])])
        else:
            raise ValueError(f"Unsupported data dimensionality: {data.ndim}D")
        
        optimal_bins = get_default_bin_count(df)
        return DataModel(df, bins=optimal_bins, label=dataset_label)

    def _create_data_label(self, dist_name: str, type_: str, n_dim: str) -> str:
        """Creates a label for newly-generated data"""
        key = dist_name + n_dim
        if key not in self.counter:
            self.counter[key] = 0
        
        self.counter[key] += 1
        counter = self.counter[key]
        
        return f"{dist_name}{type_}{n_dim}D_({counter})"