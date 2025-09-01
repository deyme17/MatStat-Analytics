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
    def __init__(self, parent, dp_widgets: list, on_data_version_changed=None, on_original_clicked=None):
        """
        Args:
            parent: The parent widget that contains this controller
            dp_widgets (list): Widget classes for data processing operations including:
                - Data transformation operations
                - Anomaly detection functionality  
                - Missing data handling operations
            on_data_version_changed (Callable[[int], None], optional): Callback for dataset version change
            on_original_clicked (Callable[[], None], optional): Callback for "Original" button click
        """
        super().__init__(parent)

        self._parent = parent
        self.dp_widgets = dp_widgets
        self.on_data_version_changed = on_data_version_changed
        self.on_original_clicked = on_original_clicked

        self._init_ui()
        self._setup_layout()

    def _init_ui(self):
        """Initialize UI components."""
        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        if self.on_data_version_changed:
            self.data_version_combo.currentIndexChanged.connect(self.on_data_version_changed)

        self.transformation_label = QLabel("Current state: Original")

        self.original_button = QPushButton("Original")
        self.original_button.setEnabled(False)
        self.original_button.setFixedSize(ORIG_BUTTON_WIDTH, ORIG_BUTTON_HEIGHT)
        if self.on_original_clicked:
            self.original_button.clicked.connect(self.on_original_clicked)

    def set_callbacks(self, on_data_version_changed=None, on_original_clicked=None):
        """
        Assign or update callbacks after initialization.
        Args:
            on_data_version_changed (Callable[[int], None], optional)
            on_original_clicked (Callable[[], None], optional)
        """
        if on_data_version_changed:
            self.on_data_version_changed = on_data_version_changed
            try:
                self.data_version_combo.currentIndexChanged.disconnect()
            except TypeError:
                pass
            self.data_version_combo.currentIndexChanged.connect(on_data_version_changed)

        if on_original_clicked:
            self.on_original_clicked = on_original_clicked
            try:
                self.original_button.clicked.disconnect()
            except TypeError:
                pass
            self.original_button.clicked.connect(on_original_clicked)

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