import numpy as np
import pandas as pd
from models.data_model import DataModel
from services.ui_services.messager import UIMessager
from services.data_services.data_version_manager import DataVersionManager

from utils.def_bins import get_default_bin_count
from utils import AppContext, EventBus, EventType


class DataSaver:
    def __init__(self):
        """
        Args:
            context (AppContext): Application context container
            on_save: Callback to applying data saving
        """
        self.counter = {}
        
    def save_data(self, dist_name: str, data: np.ndarray, type_: str = "Simulation") -> DataModel:
        """
        Save simulated data as a new dataset in the data history manager.
        Args:
            dist_name: name of the distribution
            data: simulated data array (1D or 2D)
        """
        dataset_label = self._create_data_label(dist_name, type_)
        
        if data.ndim == 1:
            df = pd.DataFrame(data, columns=['value'])
        elif data.ndim == 2:
            df = pd.DataFrame(data, columns=[f"col{i+1}" for i in range(data.shape[1])])
        else:
            raise ValueError(f"Unsupported data dimensionality: {data.ndim}D")
        
        optimal_bins = get_default_bin_count(df)
        return DataModel(df, bins=optimal_bins, label=dataset_label)

    def _create_data_label(self, dist_name: str, type_: str) -> str:
        """Creates a label for newly-generated data"""
        if dist_name not in self.counter:
            self.counter[dist_name] = 0
        
        self.counter[dist_name] += 1
        counter = self.counter[dist_name]
        
        return f"{dist_name}{type_}{counter}"