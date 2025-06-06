import os
from PyQt6.QtWidgets import QFileDialog
import pandas as pd

class DataLoaderService:
    """
    Service for selecting, loading, and postprocessing data files.
    """

    @staticmethod
    def select_file(window) -> str | None:
        """
        Open file dialog and let user select a data file.

        :param window: parent Qt window
        :return: path to selected file or None if cancelled
        """
        path, _ = QFileDialog.getOpenFileName(
            window,
            'Select the File',
            '',
            'All Supported Files (*.txt *.csv *.xlsx *.xls);;'
            'Text Files (*.txt);;CSV Files (*.csv);;'
            'Excel Files (*.xlsx *.xls);;All Files (*)'
        )
        return path if path else None

    @staticmethod
    def load_data(path: str) -> pd.Series | None:
        """
        Load numerical data from file (TXT, CSV, XLSX, XLS).

        :param path: path to the selected file
        :return: pandas Series with valid numeric data, or None on error
        """
        try:
            file_extension = os.path.splitext(path)[1].lower()

            if file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(path)
            elif file_extension == '.csv':
                df = pd.read_csv(path, decimal=',')
            elif file_extension == '.txt':
                with open(path, 'r') as file:
                    lines = [line.strip().replace(',', '.') for line in file]
                    valid_data = []
                    for x in lines:
                        if not x:
                            continue
                        try:
                            if ',' in x:
                                x = x.split(',')[1]
                            valid_data.append(float(x))
                        except ValueError:
                            print(f"Skipping invalid value: {x}")
                    if not valid_data:
                        print("No valid data found in file")
                        return None
                    return pd.Series(valid_data)
            else:
                print(f"Unsupported file type: {file_extension}")
                return None

            if len(df.columns) > 1:
                df = df.iloc[:, -1]

            df = pd.to_numeric(df, errors='coerce')
            if df.empty:
                print("No valid numerical data found in file")
                return None

            return df

        except FileNotFoundError:
            print("File not found")
            return None
        except PermissionError:
            print("Permission denied when accessing file")
            return None
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            return None