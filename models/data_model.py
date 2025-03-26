import pandas as pd
import os

class Data:
    """
    A class for handling data loading and preprocessing from various file types.
    """

    def __init__(self):
        self.data = None

    def load_data(self, path):
        """
        Loads numerical data from various file types, converting values as needed.
        
        Parameters:
            path (str): The file path to load data from.
        
        Returns:
            pd.Series: A Pandas Series containing the valid numerical data, or None if loading fails.
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
                    
                    self.data = pd.Series(valid_data)
                    return self.data
            else:
                print(f"Unsupported file type: {file_extension}")
                return None

            if len(df.columns) > 1:
                df = df.iloc[:, -1]
            
            df = pd.to_numeric(df, errors='coerce').dropna()
            
            if df.empty:
                print("No valid numerical data found in file")
                return None
            
            self.data = df
            return self.data
            
        except FileNotFoundError:
            print("File not found")
            return None
        except PermissionError:
            print("Permission denied when accessing file")
            return None
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            return None