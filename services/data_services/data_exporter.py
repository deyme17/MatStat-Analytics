from io import BytesIO
import pandas as pd
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
    def export(dist_name: str, data: pd.DataFrame, exporter_cls: IExporter = CSVExporter, out_dir: str = ".data/simulated_data") -> str:
        """
        Export data to file
        Args:
            exporter_cls: class for data exporting
            dist_name: distribution name
            data: DataFrame
            out_dir: directory to
        Returns:
            str: path to saved file
        """
        buffer = exporter_cls.export(data)

        filename = f"{dist_name.lower()}{data.shape[1]}_{len(data)}.{exporter_cls.extension}"
        filepath = f"{out_dir}/{filename}"

        os.makedirs(out_dir, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(buffer.getvalue())

        return filepath