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
        return pd.read_csv(path, decimal=',')


class TextLoader(FileLoader):
    """Loader for text files with custom parsing logic."""
    
    def load(self, path: str) -> pd.DataFrame:
        with open(path, 'r') as file:
            lines = [line.strip().replace(',', '.') for line in file]
            valid_data = []
            
            for line in lines:
                if not line:
                    continue
                try:
                    # If comma exists, take the second part
                    value = line.split(',')[1] if ',' in line else line
                    valid_data.append(float(value))
                except (ValueError, IndexError):
                    print(f"Skipping invalid value: {line}")
            
            if not valid_data:
                raise ValueError("No valid data found in file")
            
            return pd.DataFrame({'data': valid_data})