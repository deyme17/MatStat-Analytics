from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QGroupBox, QCheckBox
from typing import Any

ORIG_BUTTON_WIDTH, ORIG_BUTTON_HEIGHT = 111, 30
EXPORT_BUTTON_WIDTH, EXPORT_BUTTON_HEIGHT = 111, 30

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
                 on_original_clicked=None,
                 on_column_changed=None,
                 on_data_exported=None
                 ):
        """
        Args:
            widget_data (list[tuple[str, QGroupBox, Any]]): Widget classes for data processing operations with it's controllers
            on_data_version_changed (Callable[[int], None], optional): Callback for dataset version change
            on_column_changed (Callable[[int], None], optional): Callback for current dataframe column change
            on_original_clicked (Callable[[bool], None], optional): Callback for "Original" button click
            on_data_exported (Callable[[bool], None], optional): Callback for "Export data" button click
        """
        super().__init__()
        self.widget_data = widget_data
        self.on_data_version_changed = on_data_version_changed
        self.on_original_clicked = on_original_clicked
        self.on_column_changed = on_column_changed
        self.on_data_exported = on_data_exported

        self._init_ui()
        self._setup_layout()

    def _init_ui(self):
        """Initialize UI components."""
        def make_label(text: str) -> QLabel:
            return QLabel(text)
        
        def make_combo(callback=None) -> QComboBox:
            combo = QComboBox()
            combo.setEnabled(False)
            if callback:
                combo.currentIndexChanged.connect(callback)
            return combo
        
        def make_button(text: str, width: int, height: int, callback=None) -> QPushButton:
            btn = QPushButton(text)
            btn.setEnabled(False)
            btn.setFixedSize(width, height)
            if callback:
                btn.clicked.connect(lambda: callback(self.whole_dataset_checkbox.isChecked()))
            return btn

        self.data_version_label = make_label("Select loaded dataset:")
        self.data_version_combo = make_combo(self.on_data_version_changed)

        self.transformation_label = make_label("Current state: Original")

        self.current_col_label = make_label("Select column to apply operation to:")
        self.dataframe_cols_combo = make_combo(self.on_column_changed)

        self.whole_dataset_checkbox = QCheckBox("Whole dataset")
        self.whole_dataset_checkbox.setChecked(False)

        self.original_button = make_button(
            "Original", ORIG_BUTTON_WIDTH, ORIG_BUTTON_HEIGHT, self.on_original_clicked
        )
        self.export_data_button = make_button(
            "Export data", EXPORT_BUTTON_WIDTH, EXPORT_BUTTON_HEIGHT, self.on_data_exported
        )

    def set_callbacks(self, on_data_version_changed=None, on_original_clicked=None, on_column_changed=None, on_data_exported=None):
        """
        Assign or update callbacks after initialization.
        Args:
            on_data_version_changed (Callable[[int], None], optional)
            on_column_changed (Callable[[int], None], optional)
            on_original_clicked (Callable[[], None], optional)
        """
        def safe_connect_callback(cb):
            if cb:
                self.cb = cb
                try:
                    self.original_button.clicked.disconnect()
                except TypeError:
                    pass
                self.original_button.clicked.connect(cb)

        safe_connect_callback(on_data_version_changed)
        safe_connect_callback(on_original_clicked)
        safe_connect_callback(on_column_changed)
        safe_connect_callback(on_data_exported)

    def _setup_layout(self):
        """Setup the main layout structure."""
        # Navigation layout for the button
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.original_button)
        nav_layout.addWidget(self.export_data_button)
        nav_layout.addWidget(self.whole_dataset_checkbox)
        nav_layout.addStretch()

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.data_version_label)
        layout.addWidget(self.data_version_combo)
        layout.addWidget(self.transformation_label)
        layout.addWidget(self.current_col_label)
        layout.addWidget(self.dataframe_cols_combo)

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