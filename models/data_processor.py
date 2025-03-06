class DataProcessor:
    def __init__(self):
        self.data_history = []  
        self.transformed_data = None 
        self.current_index = -1  
        self.current_transformation = "Original"

    def add_data(self, data, filename="New Data"):
        """Add a new loaded dataset (not transformations)"""
        self.data_history.append((filename, data.copy()))
        self.current_index = len(self.data_history) - 1
        self.reset_transformation()
        return data

    def is_transformed(self):
        """Check if the data has been transformed"""
        return self.transformed_data is not None

    def reset_transformation(self):
        """Resets the data version to the origin"""
        self.transformed_data = None
        self.current_transformation = "Original"

    def standardize_data(self, data):
        """Standardize the data"""
        from utils.stat_func import standardize_data
        self.transformed_data = standardize_data(data)
        self.current_transformation = "Standardized"
        return self.transformed_data

    def log_transform_data(self, data):
        """Logarithmization"""
        from utils.stat_func import log_transform_data
        self.transformed_data = log_transform_data(data)
        self.current_transformation = "Log Transform"
        return self.transformed_data

    def shift_data(self, data, shift_value):
        """Shifts the data"""
        from utils.stat_func import shift_data
        self.transformed_data = shift_data(data, shift_value)
        self.current_transformation = f"Shifted by {shift_value}"
        return self.transformed_data

    def get_previous_data(self):
        """Go to previous dataset (not transformation)"""
        if self.current_index > 0:
            self.current_index -= 1
            self.reset_transformation()
            return self.data_history[self.current_index][1]
        return None

    def get_next_data(self):
        """Go to next dataset (not transformation)"""
        if self.current_index < len(self.data_history) - 1:
            self.current_index += 1
            self.reset_transformation()
            return self.data_history[self.current_index][1]
        return None

    def get_original_data(self):
        """Go to original version of current dataset"""
        self.reset_transformation()
        return self.data_history[self.current_index][1]

    def get_current_data(self):
        """Get current dataset with any applied transformations"""
        if self.current_index >= 0:
            if self.transformed_data is not None:
                return self.transformed_data
            return self.data_history[self.current_index][1]
        return None

    def get_data_description(self):
        """Get description of current data state"""
        if self.current_index >= 0:
            base_name = self.data_history[self.current_index][0]
            if self.current_transformation != "Original":
                return f"{base_name} ({self.current_transformation})"
            return base_name
        return "No Data"

    def get_all_data_descriptions(self):
        """Get all loaded datasets (not transformations)"""
        return [desc for desc, _ in self.data_history]

    def get_current_transformation(self):
        """Get current transformation description"""
        return self.current_transformation