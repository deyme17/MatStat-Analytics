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
    def export(cls, name: str, data: np.ndarray|pd.DataFrame, exporter_cls: IExporter = CSVExporter, out_dir: str = "data/simulated_data") -> str:
        """
        Export data to file
        Args:
            name: data name
            data: ndarray (1D or 2D)
            exporter_cls: class for data exporting
            out_dir: directory to save file
        Returns:
            str: path to saved file
        """
        if isinstance(data, pd.DataFrame):
            df = data
            n_cols = data.shape[1]
        elif isinstance(data, np.ndarray):
            if data.ndim == 1:
                df = pd.DataFrame(data, columns=['value'])
                n_cols = 1
            elif data.ndim == 2:
                df = pd.DataFrame(data, columns=[f'x{i+1}' for i in range(data.shape[1])])
                n_cols = data.shape[1]
            else:
                raise ValueError(f"Unsupported array dimensionality: {data.ndim}D. Only 1D and 2D arrays are supported.")
        else:
            raise TypeError("Data must be either a pandas DataFrame or numpy ndarray.")
        
        buffer = exporter_cls.export(df)

        filename = f"{name.lower()}_({n_cols},{len(df)}).{exporter_cls.extension}"
        out_dir = os.path.normpath(out_dir)
        filepath = os.path.join(out_dir, filename)

        os.makedirs(out_dir, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(buffer.getvalue())

        return filepath