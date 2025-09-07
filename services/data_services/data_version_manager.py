class DataVersionManager:
    """
    Manager for handling multiple datasets (DataModel instances).
    Each dataset maintains its own transformation history.
    """
    def __init__(self):
        """
        Initialize an empty dataset manager.
        """
        self.datasets = {}        # {dataset_name: DataModel (current version)}
        self.current_dataset_name = None   # name of active dataset

    def add_dataset(self, dataset_name: str, model):
        """
        Add a new dataset and set it as current.
        Args:
            dataset_name: name of the dataset file/source
            model: DataModel instance (should be original version)
        """
        self.datasets[dataset_name] = model
        self.current_dataset_name = dataset_name

    def switch_to_dataset(self, dataset_name: str):
        """
        Switch to a previously added dataset by its name.
        Args:
            dataset_name: name of dataset to switch to
        """
        if dataset_name in self.datasets:
            self.current_dataset_name = dataset_name

    def get_current_data_model(self):
        """
        Return the currently active DataModel (current version).
        """
        if self.current_dataset_name and self.current_dataset_name in self.datasets:
            return self.datasets[self.current_dataset_name]
        return None

    def update_current_dataset(self, new_model):
        """
        Replace the current dataset's model with a new version.
        Args:
            new_model: new DataModel instance (transformed version)
        """
        if self.current_dataset_name:
            self.datasets[self.current_dataset_name] = new_model

    def get_all_dataset_names(self) -> list[str]:
        """
        Return all names of stored datasets.
        """
        return list(self.datasets.keys())

    def get_current_dataset_name(self) -> str:
        """
        Return the name of the current dataset.
        """
        return self.current_dataset_name or "No Dataset"

    def has_datasets(self) -> bool:
        """
        Check if any datasets are loaded.
        """
        return len(self.datasets) > 0