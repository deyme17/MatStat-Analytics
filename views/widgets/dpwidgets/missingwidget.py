from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QLabel
from controllers.missing_controller import MissingDataController
from utils.ui_styles import groupStyle

class MissingWidget(QGroupBox):
    def __init__(self, window):
        super().__init__("Missing Data")
        self.setStyleSheet(groupStyle)
        layout = QVBoxLayout()

        window.missing_controller = MissingDataController(window)

        window.missing_count_label = QLabel("Total Missing: 0")
        window.missing_percentage_label = QLabel("Missing Percentage: 0.00%")

        window.impute_mean_button = QPushButton("Replace with Mean")
        window.impute_mean_button.setEnabled(False)
        window.impute_mean_button.clicked.connect(window.missing_controller.impute_with_mean)

        window.impute_median_button = QPushButton("Replace with Median")
        window.impute_median_button.setEnabled(False)
        window.impute_median_button.clicked.connect(window.missing_controller.impute_with_median)

        window.interpolate_linear_button = QPushButton("Interpolate (Linear)")
        window.interpolate_linear_button.setEnabled(False)
        window.interpolate_linear_button.clicked.connect(
            lambda: window.missing_controller.interpolate_missing("linear")
        )

        window.drop_missing_button = QPushButton("Drop Missing Values")
        window.drop_missing_button.setEnabled(False)
        window.drop_missing_button.clicked.connect(window.missing_controller.drop_missing_values)

        layout.addWidget(window.missing_count_label)
        layout.addWidget(window.missing_percentage_label)
        layout.addWidget(window.impute_mean_button)
        layout.addWidget(window.impute_median_button)
        layout.addWidget(window.interpolate_linear_button)
        layout.addWidget(window.drop_missing_button)
        self.setLayout(layout)