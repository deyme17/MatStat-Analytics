from .base_dp_widget import BaseDataWidget
from PyQt6.QtWidgets import QPushButton, QLabel


class MissingWidget(BaseDataWidget):
    """Widget for handling missing data in the dataset."""
    def __init__(self, controller):
        super().__init__("Missing Data", controller)
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components."""
        # Info labels
        self.missing_count_label = QLabel("Total Missing: 0")
        self.missing_percentage_label = QLabel("Missing Percentage: 0.00%")
        self.add_widget(self.missing_count_label)
        self.add_widget(self.missing_percentage_label)
        
        # Action buttons
        buttons_config = [
            ("impute_mean_button", "Replace with Mean", 
             self.controller.impute_with_mean),
            ("impute_median_button", "Replace with Median", 
             self.controller.impute_with_median),
            ("interpolate_linear_button", "Interpolate (Linear)", 
             lambda: self.controller.interpolate_missing("linear")),
            ("drop_missing_button", "Drop Missing Values", 
             self.controller.drop_missing_values)
        ]
        
        for attr_name, text, callback in buttons_config:
            button = QPushButton(text)
            button.setEnabled(False)
            button.clicked.connect(callback)
            setattr(self, attr_name, button)
            self.add_widget(button)