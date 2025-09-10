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
    def export(dist_name: str, data: np.ndarray, exporter_cls: IExporter = CSVExporter, out_dir: str = ".data/simulated_data") -> str:
        """
        Export data to file
        Args:
            exporter_cls: class for data exporting
            dist_name: distribution name
            data: ndarray
            out_dir: directory to
        Returns:
            str: path to saved file
        """
        df = pd.DataFrame(data)
        buffer = exporter_cls.export(df)

        filename = f"{dist_name.lower()}{df.shape[1]}_{len(df)}.{exporter_cls.extension}"
        filepath = f"{out_dir}/{filename}"

        os.makedirs(out_dir, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(buffer.getvalue())

        return filepath