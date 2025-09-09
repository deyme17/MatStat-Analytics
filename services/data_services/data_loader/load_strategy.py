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
        for sep in [',', ';', '\t']:
            try:
                return pd.read_csv(path, sep=sep)
            except Exception:
                continue
        return TextLoader().load(path)


class TextLoader(FileLoader):
    """Loader for text files with custom parsing logic."""
    def load(self, path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(path, header=None, delim_whitespace=True)
            if df.apply(lambda x: pd.to_numeric(x, errors='coerce').notna()).all().all():
                return df
        except Exception:
            pass
            
        try:
            df = pd.read_csv(path, header=None)
            return df
        except Exception:
            pass
        
        with open(path, 'r') as file:
            lines = []
            for line in file:
                line = line.strip().replace(",", ".")
                if line:
                    parts = line.split()
                    if parts:
                        try:
                            row_values = [float(part) for part in parts]
                            lines.append(row_values)
                        except ValueError:
                            print(f"Skipping invalid line: {line}")
            
            if not lines:
                raise ValueError("No valid data found in file")
            
            max_cols = max(len(row) for row in lines)
            
            if max_cols == 1:
                return pd.DataFrame({"data": [row[0] for row in lines]})
            else:
                padded_lines = []
                for row in lines:
                    padded_row = row + [None] * (max_cols - len(row))
                    padded_lines.append(padded_row)
                return pd.DataFrame(padded_lines)