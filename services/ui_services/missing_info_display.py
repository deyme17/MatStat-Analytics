class MissingInfoDisplayService:
    """Displays missing data info in UI labels."""
    
    def __init__(self, count_label, percent_label):
        """
        Args:
            count_label: Shows total missing values count
            percent_label: Shows missing values percentage
        """
        self.count_label = count_label
        self.percent_label = percent_label

    def update(self, info: dict):
        """Updates labels with current missing data stats.
        Args:
            info: {'total_missing': int, 'missing_percentage': float}
        """
        self.count_label.setText(f"Total Missing: {info['total_missing']}")
        self.percent_label.setText(f"Missing Percentage: {info['missing_percentage']:.2f}%")