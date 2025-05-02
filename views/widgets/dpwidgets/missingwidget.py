from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QPushButton, QLabel
from controllers.missing_controller import MissingDataController
from utils.ui_styles import groupStyle

class MissingWidget(QGroupBox):
    def __init__(self, parent):
        super().__init__("Missing Data")
        self.setStyleSheet(groupStyle)
        layout = QVBoxLayout()

        parent.missing_controller = MissingDataController(parent)

        parent.missing_count_label = QLabel("Total Missing: 0")
        parent.missing_percentage_label = QLabel("Missing Percentage: 0.00%")

        parent.impute_mean_button = QPushButton("Replace with Mean")
        parent.impute_mean_button.setEnabled(False)
        parent.impute_mean_button.clicked.connect(parent.missing_controller.impute_with_mean)

        parent.impute_median_button = QPushButton("Replace with Median")
        parent.impute_median_button.setEnabled(False)
        parent.impute_median_button.clicked.connect(parent.missing_controller.impute_with_median)

        parent.interpolate_linear_button = QPushButton("Interpolate (Linear)")
        parent.interpolate_linear_button.setEnabled(False)
        parent.interpolate_linear_button.clicked.connect(
            lambda: parent.missing_controller.interpolate_missing("linear")
        )

        parent.drop_missing_button = QPushButton("Drop Missing Values")
        parent.drop_missing_button.setEnabled(False)
        parent.drop_missing_button.clicked.connect(parent.missing_controller.drop_missing_values)

        layout.addWidget(parent.missing_count_label)
        layout.addWidget(parent.missing_percentage_label)
        layout.addWidget(parent.impute_mean_button)
        layout.addWidget(parent.impute_median_button)
        layout.addWidget(parent.interpolate_linear_button)
        layout.addWidget(parent.drop_missing_button)
        self.setLayout(layout)