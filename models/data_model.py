import pandas as pd
import numpy as np

class Data:
    def __init__(self):
        self.data = None

    def load_data(self, path):
        try:
            with open(path, 'r') as file:
                lines = [line.strip().replace(',', '.') for line in file]
                self.data = pd.Series([float(x) for x in lines if x])
            return self.data
            
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            return None