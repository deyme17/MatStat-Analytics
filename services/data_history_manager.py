class DataHistoryManager:
    def __init__(self):
        self.datasets = {}        # {label: DataModel}
        self.current_key = None   # label of active dataset

    def add_dataset(self, label: str, model):
        self.datasets[label] = model
        self.current_key = label

    def switch_to(self, label: str):
        if label in self.datasets:
            self.current_key = label

    def get_current_data(self):
        if self.current_key and self.current_key in self.datasets:
            return self.datasets[self.current_key]
        return None

    def get_original_data(self):
        current = self.get_current_data()
        return current.revert_to_original() if current else None

    def update_current_data(self, new_model):
        if self.current_key:
            self.datasets[self.current_key] = new_model

    def get_all_descriptions(self):
        return list(self.datasets.keys())

    def get_data_description(self):
        return self.current_key or "Unnamed"
