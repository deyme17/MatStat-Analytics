from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QGroupBox
from typing import Any

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
    def __init__(self, widget_data: list[tuple[str, QGroupBox, Any]], 
                 on_data_version_changed=None, 
                 on_original_clicked=None
                 ):
        """
        Args:
            widget_data (list[tuple[str, QGroupBox, Any]]): Widget classes for data processing operations with it's controllers
            on_data_version_changed (Callable[[int], None], optional): Callback for dataset version change
            on_original_clicked (Callable[[], None], optional): Callback for "Original" button click
        """
        super().__init__()
        self.widget_data = widget_data
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
        for name, widget_cls, controller in self.widget_data:
            widget = widget_cls(controller)
            setattr(self, name, widget)
            layout.addWidget(widget)