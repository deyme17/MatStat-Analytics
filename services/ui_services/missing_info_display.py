class MissingInfoDisplayService:
    """Displays missing data info in UI labels."""
    def __init__(self, set_count_label, set_percent_label):
        """
        Args:
            set_count_label: Function that set total missing values count text 
            set_percent_label: Function that set missing values percentage text
        """
        self.set_count_label = set_count_label
        self.set_percent_label = set_percent_label

    def update(self, info: dict):
        """Updates labels with current missing data stats.
        Args:
            info: {'total_missing': int, 'missing_percentage': float}
        """
        self.set_count_label(f"Total Missing: {info['total_missing']}")
        self.set_percent_label(f"Missing Percentage: {info['missing_percentage']:.2f}%")