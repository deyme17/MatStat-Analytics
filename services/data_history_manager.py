class DataHistoryManager:
    def __init__(self):
        self.data_history = []
        self.current_index = -1

    def add_data(self, data, name="Unnamed"):
        self.data_history.append({
            'name': name,
            'data': data.copy(),
            'original': data.copy(),
            'transform_state': {
                'transformed_data': None,
                'transformation_steps': [],
                'current_transformation': "Original"
            }
        })
        self.current_index = len(self.data_history) - 1

    def get_current_data(self):
        if 0 <= self.current_index < len(self.data_history):
            return self.data_history[self.current_index]['data'].copy()
        return None

    def get_original_data(self):
        if 0 <= self.current_index < len(self.data_history):
            return self.data_history[self.current_index]['original'].copy()
        return None

    def update_current_data(self, new_data):
        if 0 <= self.current_index < len(self.data_history):
            self.data_history[self.current_index]['data'] = new_data.copy()

    def get_data_description(self):
        if 0 <= self.current_index < len(self.data_history):
            return self.data_history[self.current_index]['name']
        return "Unnamed"

    def get_all_descriptions(self):
        return [entry['name'] for entry in self.data_history]

    def get_transform_state(self):
        if 0 <= self.current_index < len(self.data_history):
            return self.data_history[self.current_index]['transform_state']
        return {
            'transformed_data': None,
            'transformation_steps': [],
            'current_transformation': "Original"
        }

    def set_transform_state(self, state):
        if 0 <= self.current_index < len(self.data_history):
            self.data_history[self.current_index]['transform_state'] = state
