from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout

ORIG_BUTTON_WIDTH, ORIG_BUTTON_HEIGHT = 333, 30

class DataProcessingTab(QWidget):
    """
    A UI tab for managing data preprocessing steps including:
    - Data version selection
    - Transformations
    - Anomaly detection
    - Missing data handling
    - Original data restoration
    """

    def __init__(self, parent, processor_widget, anomaly_widget, missing_widget):
        """
        Args:
            parent: The parent widget that contains this controller
            processor_widget: Widget class for data processing/transformation operations
            anomaly_widget: Widget class for anomaly detection functionality
            missing_widget: Widget class for handling missing data operations
        """
        super().__init__(parent)

        # Data version controls
        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        self.data_version_combo.currentIndexChanged.connect(
            parent.data_version_controller.on_data_version_changed
        )

        # Transformation state label
        self.transformation_label = QLabel("Current state: Original")

        # Original data button
        self.original_button = QPushButton("Original")
        self.original_button.setEnabled(False)
        self.original_button.setFixedSize(ORIG_BUTTON_WIDTH, ORIG_BUTTON_HEIGHT)
        self.original_button.clicked.connect(parent.data_version_controller.original_data)

        # Navigation layout for the button
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.original_button)
        nav_layout.addStretch()

        # Preprocessing widgets
        self.process_controls = processor_widget(parent)
        self.anomaly_detection = anomaly_widget(parent)
        self.missing_data = missing_widget(parent)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.data_version_label)
        layout.addWidget(self.data_version_combo)
        layout.addWidget(self.transformation_label)
        layout.addWidget(self.process_controls)
        layout.addWidget(self.anomaly_detection)
        layout.addWidget(self.missing_data)
        layout.addLayout(nav_layout)
        layout.addStretch()

        self.setLayout(layout)

        # Expose widgets to parent for controller access
        parent.data_version_label = self.data_version_label
        parent.data_version_combo = self.data_version_combo
        parent.transformation_label = self.transformation_label
        parent.original_button = self.original_button