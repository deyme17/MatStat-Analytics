from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from utils.ui_styles import groupStyle
from views.widgets.dpwidgets.processdatawidget import ProcessDataWidget
from views.widgets.dpwidgets.anomalywidget import AnomalyWidget
from views.widgets.dpwidgets.missingwidget import MissingWidget


class DataProcessingTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        self.data_version_combo.currentIndexChanged.connect(parent.ui_controller.on_data_version_changed)

        self.transformation_label = QLabel("Current state: Original")

        self.process_controls = ProcessDataWidget(parent)
        self.anomaly_detection = AnomalyWidget(parent)
        self.missing_data = MissingWidget(parent)

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

        parent.data_version_label = self.data_version_label
        parent.data_version_combo = self.data_version_combo
        parent.transformation_label = self.transformation_label