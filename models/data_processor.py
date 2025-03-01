from utils.stat_func import standardize_data, log_transform_data, shift_data
import numpy as np
import pandas as pd

class DataProcessor:

    def __init__(self):
        self.data_history = []
        self.current_index = -1
        self.original_data = None
        
    def add_data(self, data):
        # save origin data
        if self.original_data is None:
            self.original_data = data.copy()
            self.data_history = [("Original Data", data.copy())]
            self.current_index = 0
        else:
            if self.current_index < len(self.data_history) - 1:
                self.data_history = self.data_history[:self.current_index + 1]
            # new data to history
            self.data_history.append(("New Data", data.copy()))
            self.current_index = len(self.data_history) - 1
    
    def standardize_data(self, data):
        """Standardize the data"""
        processed_data = standardize_data(data)
        self.data_history.append(("Standardized", processed_data))
        self.current_index = len(self.data_history) - 1
        return processed_data

    def log_transform_data(self, data):
        """Logarithmization"""
        processed_data = log_transform_data(data)
        self.data_history.append(("Log Transform", processed_data))
        self.current_index = len(self.data_history) - 1
        return processed_data

    def shift_data(self, data, shift_value):
        """Shifts the data"""
        processed_data = shift_data(data, shift_value)
        self.data_history.append((f"Shifted by {shift_value}", processed_data))
        self.current_index = len(self.data_history) - 1
        return processed_data
    
    def get_previous_data(self):
        """Go to prev version of data"""
        if self.current_index > 0:
            self.current_index -= 1
            return self.data_history[self.current_index][1]
        return None
    
    def get_next_data(self):
        """Go to next version of data"""
        if self.current_index < len(self.data_history) - 1:
            self.current_index += 1
            return self.data_history[self.current_index][1]
        return None
    
    def get_original_data(self):
        """Go to origin data"""
        self.current_index = 0
        return self.data_history[0][1]
    
    def get_current_data(self):
        """Go to current data"""
        if self.current_index >= 0:
            return self.data_history[self.current_index][1]
        return None
    
    def get_data_description(self):
        """Get description of data"""
        if self.current_index >= 0:
            return self.data_history[self.current_index][0]
        return "No Data"
        
    def get_all_data_descriptions(self):
        """Get all versions of data"""
        return [desc for desc, _ in self.data_history]