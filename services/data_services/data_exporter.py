from io import BytesIO
import pandas as pd
import numpy as np
import os
from abc import ABC, abstractmethod


class IExporter(ABC):
    extension: str
    @staticmethod
    @abstractmethod
    def export(data: pd.DataFrame) -> BytesIO:
        pass

class CSVExporter(IExporter):
    extension = "csv"
    @staticmethod
    def export(data: pd.DataFrame) -> BytesIO:
        buffer = BytesIO()
        data.to_csv(buffer, index=False)
        buffer.seek(0)
        return buffer


class DataExporter:
    @classmethod
    def export(cls, dist_name: str, data: np.ndarray, exporter_cls: IExporter = CSVExporter, out_dir: str = "data/simulated_data") -> str:
        """
        Export data to file
        Args:
            dist_name: distribution name
            data: ndarray (1D or 2D)
            exporter_cls: class for data exporting
            out_dir: directory to save file
        Returns:
            str: path to saved file
        """
        if data.ndim == 1:
            df = pd.DataFrame(data, columns=['value'])
            n_cols = 1
        elif data.ndim == 2:
            df = pd.DataFrame(data, columns=[f'col{i+1}' for i in range(data.shape[1])])
            n_cols = data.shape[1]
        else:
            raise ValueError(f"Unsupported data dimensionality: {data.ndim}D. Only 1D and 2D arrays are supported.")
        
        buffer = exporter_cls.export(df)

        filename = f"{dist_name.lower()}{n_cols}_{len(df)}.{exporter_cls.extension}"
        filepath = os.path.join(out_dir, filename)

        os.makedirs(out_dir, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(buffer.getvalue())

        return filepath