import os
from services.data_services.data_loader import loaders
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
        
        :param extension: File extension (e.g., '.json')
        :param loader: FileLoader instance
        """
        self._loaders[extension.lower()] = loader
    
    def get_supported_extensions(self) -> list[str]:
        """Get list of supported file extensions."""
        return list(self._loaders.keys())
    
    def load_data(self, path: str) -> Optional[pd.Series]:
        """
        Load numerical data from file.

        :param path: path to the selected file
        :return: pandas Series with valid numeric data, or None on error
        """
        try:
            file_extension = os.path.splitext(path)[1].lower()
            
            if file_extension not in self._loaders:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            # Load data using appropriate loader
            loader = self._loaders[file_extension]
            df = loader.load(path)
            
            # Process the DataFrame to Series
            series = self.process_dataframe(df)
            
            return series
            
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
    def process_dataframe(df: pd.DataFrame) -> pd.Series:
        """
        Convert DataFrame to Series with numeric data.
        
        :param df: Input DataFrame
        :return: pandas Series with numeric data
        """
        # Take the last column if multiple columns exist
        if len(df.columns) > 1:
            df = df.iloc[:, -1]
        else:
            df = df.iloc[:, 0]
        
        # Convert to numeric, replacing invalid values with NaN
        series = pd.to_numeric(df, errors='coerce')
        
        if series.empty or series.isna().all():
            raise ValueError("No valid numerical data found")
        
        return series
    
    @staticmethod
    def select_file(parent=None) -> Optional[str]:
        """
        Open file dialog and let user select a data file.

        :param parent: parent Qt widget (optional)
        :return: path to selected file or None if cancelled
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