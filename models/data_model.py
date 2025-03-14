import pandas as pd

class Data:
    """
    A class for handling data loading and preprocessing from a text file.
    """

    def __init__(self):
        self.data = None

    def load_data(self, path):
        """
        Loads numerical data from a text file, converting values from string format.
        
        Parameters:
            path (str): The file path to load data from.
        
        Returns:
            pd.Series: A Pandas Series containing the valid numerical data, or None if loading fails.
        """
        
        try:
            with open(path, 'r') as file:
                lines = [line.strip().replace(',', '.') for line in file]

                valid_data = []
                for x in lines:
                    if not x:
                        continue
                    
                    try:
                        valid_data.append(float(x))
                    except ValueError:
                        print(f"Skipping invalid value: {x}")
                
                if not valid_data:
                    print("No valid data found in file")
                    return None
                
                self.data = pd.Series(valid_data)
                
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