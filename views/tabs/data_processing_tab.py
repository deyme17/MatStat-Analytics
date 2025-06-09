from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from utils.ui_styles import groupStyle


class DataProcessingTab(QWidget):
    """
    A UI tab for managing data preprocessing steps including:
    """

    def __init__(self, parent, processor_widget, anomaly_widget, missing_widget):
        """
        :param parent: The parent widget that contains this controller
        :param processor_widget: Widget class for data processing/transformation operations
        :param anomaly_widget: Widget class for anomaly detection functionality
        :param missing_widget: Widget class for handling missing data operations
        """
        super().__init__(parent)

        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        self.data_version_combo.currentIndexChanged.connect(
            parent.data_version_controller.on_data_version_changed
        )

        self.transformation_label = QLabel("Current state: Original")

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
        layout.addLayout(parent._create_nav_layout())
        layout.addStretch()

        self.setLayout(layout)

        # Expose widgets to parent for controller access
        parent.data_version_label = self.data_version_label
        parent.data_version_combo = self.data_version_combo
        parent.transformation_label = self.transformation_label
