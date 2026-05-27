import os
from services.data_services.data_loader import loaders
from utils.helpers import validate_feature_names
from typing import Optional
import pandas as pd


class DataLoaderService:
    """
    Service for loading and processing data files.
    Uses strategy pattern for different file types.
    """
    def __init__(self):
        self._loaders = loaders 

    def register_loader(self, extension: str, loader) -> None:
        """
        Register a new file loader for specific extension.
        Args:
            extension: File extension (e.g., '.json')
            loader: FileLoader instance
        """
        self._loaders[extension.lower()] = loader
    
    def get_supported_extensions(self) -> list[str]:
        """Get list of supported file extensions."""
        return list(self._loaders.keys())
    
    def load_data(self, path: str) -> Optional[pd.DataFrame]:
        """
        Load numerical data from file.
        Args:
            path: path to the selected file
        Return:
            pandas DataFrame with valid numeric data, or None on error
        """
        try:
            file_extension = os.path.splitext(path)[1].lower()
            
            if file_extension not in self._loaders:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            loader = self._loaders[file_extension]
            header = 0 if self._detect_header(path) else None
            df = loader.load(path, header=header)

            df = self.process_dataframe(df)
            return df

        except FileNotFoundError:
            print(f"File not found: {path}")
            return None
        except PermissionError:
            print(f"Permission denied when accessing file: {path}")
            return None
        except ValueError as e:
            print(f"Data processing error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error loading file: {str(e)}")
            return None

    @staticmethod
    def _detect_header(path: str) -> bool:
        """Returns True if the first line looks like a header (contains non-numeric tokens)."""
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                first_line = f.readline().strip()
            if not first_line:
                return False
            tokens = first_line.replace(';', ',').replace('\t', ',').split(',')
            tokens = [t.strip() for t in tokens if t.strip()]

            def is_numeric(v: str) -> bool:
                try:
                    float(v.replace(',', '.'))
                    return True
                except ValueError:
                    return False

            return any(not is_numeric(t) for t in tokens)
        except Exception:
            return False

    @staticmethod
    def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:       
        named_cols = [c for c in df.columns if isinstance(c, str)
                      and not c.lstrip('-').replace('.', '', 1).isdigit()]

        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.dropna(axis=1, how='all')
        if df.empty:
            raise ValueError("No valid numerical data found")
        
        df = df.reset_index(drop=True)
        if named_cols and len(named_cols) == df.shape[1]:
            df.columns = named_cols
        elif df.columns.isnull().any() or not validate_feature_names(list(df.columns)):
            df.columns = ["x"] if df.shape[1] == 1 else [f"x{i+1}" for i in range(df.shape[1])]

        return df

    @staticmethod
    def select_file(parent=None) -> Optional[str]:
        """
        Open file dialog and let user select a data file.

            parent: parent Qt widget (optional)
        Return:
            path to selected file or None if cancelled
        """
        from PyQt6.QtWidgets import QFileDialog
        
        path, _ = QFileDialog.getOpenFileName(
            parent,
            'Select the File',
            '',
            'All Supported Files (*.txt *.csv *.xlsx *.xls);;'
            'Text Files (*.txt);;CSV Files (*.csv);;'
            'Excel Files (*.xlsx *.xls);;All Files (*)'
        )
        return path if path else None