from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QLabel
from utils.ui_styles import groupStyle

class MissingWidget(QGroupBox):
    """
    Widget for handling missing data in the dataset.
    """

    def __init__(self, window):
        super().__init__("Missing Data")
        self.setStyleSheet(groupStyle)
        layout = QVBoxLayout()

        # Labels to display missing data info
        window.missing_count_label = QLabel("Total Missing: 0")
        window.missing_percentage_label = QLabel("Missing Percentage: 0.00%")

        # Button to replace with mean
        window.impute_mean_button = QPushButton("Replace with Mean")
        window.impute_mean_button.setEnabled(False)
        window.impute_mean_button.clicked.connect(window.missing_controller.impute_with_mean)

        # Button to replace with median
        window.impute_median_button = QPushButton("Replace with Median")
        window.impute_median_button.setEnabled(False)
        window.impute_median_button.clicked.connect(window.missing_controller.impute_with_median)

        # Button to interpolate linearly
        window.interpolate_linear_button = QPushButton("Interpolate (Linear)")
        window.interpolate_linear_button.setEnabled(False)
        window.interpolate_linear_button.clicked.connect(
            lambda: window.missing_controller.interpolate_missing("linear")
        )

        # Button to drop missing values
        window.drop_missing_button = QPushButton("Drop Missing Values")
        window.drop_missing_button.setEnabled(False)
        window.drop_missing_button.clicked.connect(window.missing_controller.drop_missing_values)

        # Add all widgets to the layout
        layout.addWidget(window.missing_count_label)
        layout.addWidget(window.missing_percentage_label)
        layout.addWidget(window.impute_mean_button)
        layout.addWidget(window.impute_median_button)
        layout.addWidget(window.interpolate_linear_button)
        layout.addWidget(window.drop_missing_button)
        self.setLayout(layout)
