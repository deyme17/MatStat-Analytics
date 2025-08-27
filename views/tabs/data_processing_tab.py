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
    def __init__(self, parent, dp_widgets: list):
        """
        Args:
            parent: The parent widget that contains this controller
            dp_widgets (list): Widget classes for data processing operations including:
                - Data transformation operations
                - Anomaly detection functionality  
                - Missing data handling operations
        """
        super().__init__(parent)
        
        self._parent = parent
        self.dp_widgets = dp_widgets
        
        self._init_ui()
        self._setup_layout()
        self._expose_widgets_to_parent()

    def _init_ui(self):
        """Initialize UI components."""
        # Data version controls
        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        self.data_version_combo.currentIndexChanged.connect(
            self._parent.data_version_controller.on_data_version_changed
        )

        # Transformation state label
        self.transformation_label = QLabel("Current state: Original")

        # Original data button
        self.original_button = QPushButton("Original")
        self.original_button.setEnabled(False)
        self.original_button.setFixedSize(ORIG_BUTTON_WIDTH, ORIG_BUTTON_HEIGHT)
        self.original_button.clicked.connect(self._parent.data_version_controller.original_data)

    def _setup_layout(self):
        """Setup the main layout structure."""
        # Navigation layout for the button
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.original_button)
        nav_layout.addStretch()

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.data_version_label)
        layout.addWidget(self.data_version_combo)
        layout.addWidget(self.transformation_label)

        # Add preprocessing widgets
        self._add_preprocessing_widgets(layout)
        
        layout.addLayout(nav_layout)
        layout.addStretch()

        self.setLayout(layout)

    def _add_preprocessing_widgets(self, layout: QVBoxLayout):
        """Add all preprocessing widgets to the layout.
        Args:
            layout (QVBoxLayout): The main layout to add widgets to
        """
        for widget_cls in self.dp_widgets:
            widget = widget_cls(self._parent)
            layout.addWidget(widget)

    def _expose_widgets_to_parent(self):
        """Expose widgets to parent for controller access."""
        self._parent.data_version_label = self.data_version_label
        self._parent.data_version_combo = self.data_version_combo
        self._parent.transformation_label = self.transformation_label
        self._parent.original_button = self.original_button