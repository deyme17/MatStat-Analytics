from abc import ABC, abstractmethod
import pandas as pd


class FileLoader(ABC):
    """Abstract base class for file loaders."""
    @abstractmethod
    def load(self, path: str) -> pd.DataFrame:
        """Load data from file and return DataFrame."""
        pass


class ExcelLoader(FileLoader):
    """Loader for Excel files (.xlsx, .xls)."""
    def load(self, path: str) -> pd.DataFrame:
        return pd.read_excel(path)


class CSVLoader(FileLoader):
    """Loader for CSV files."""
    def load(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path, sep=None, engine="python", decimal=",")


class TextLoader(FileLoader):
    """Loader for text files with custom parsing logic."""
    def load(self, path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(path, sep=None, engine="python", decimal=".")
        except Exception:
            with open(path, 'r') as file:
                values = []
                for line in file:
                    line = line.strip().replace(",", ".")
                    if line:
                        try:
                            values.append(float(line))
                        except ValueError:
                            print(f"Skipping invalid value: {line}")
                if not values:
                    raise ValueError("No valid data found in file")
                return pd.DataFrame({"data": values})