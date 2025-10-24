from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QGroupBox, QCheckBox
from typing import Any
from models.data_model import DataModel
from utils import EventBus, EventType, Event, AppContext

ORIG_BUTTON_WIDTH, ORIG_BUTTON_HEIGHT = 222, 30



class DataProcessingTab(QWidget):
    """
    A UI tab for managing data preprocessing steps including:
    - Data version selection
    - Transformations
    - Anomaly detection
    - Missing data handling
    - Original data restoration
    """
    def __init__(self, context: AppContext, widget_data: list[tuple[str, QGroupBox, Any]]):
        """
        Args:
            context: Shared application context (version_manager, event_bus, messager)
            widget_data (list[tuple[str, QGroupBox, Any]]): Widget classes for data processing operations with it's controllers
        """
        super().__init__()
        self.event_bus: EventBus = context.event_bus
        self.data_model: DataModel = context.data_model
        self.widget_data = widget_data

        self._init_ui()
        self._setup_layout()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.DATA_TRANSFORMED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.COLUMN_CHANGED, self._on_data_changed)

    def _on_data_changed(self, event: Event) -> None:
        self._update_original_button_state()
        self._update_transformation_label()

    def _init_ui(self) -> None:
        """Initialize UI components."""
        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        self.data_version_combo.currentIndexChanged.connect(lambda: self.event_bus.emit_type(EventType.DATASET_CHANGED))

        self.transformation_label = QLabel("Current state: Original")

        self.current_col_label = QLabel("Select column to apply operation to: ")
        self.dataframe_cols_combo = QComboBox()
        self.dataframe_cols_combo.setEnabled(False)
        self.dataframe_cols_combo.currentIndexChanged.connect(lambda: self.event_bus.emit_type(EventType.COLUMN_CHANGED))

        self.whole_dataset_checkbox = QCheckBox("Whole dataset")
        self.whole_dataset_checkbox.setChecked(False)

        self.original_button = QPushButton("Original")
        self.original_button.setEnabled(False)
        self.original_button.setFixedSize(ORIG_BUTTON_WIDTH, ORIG_BUTTON_HEIGHT)
        self.original_button.clicked.connect(self._on_original_button_clicked)

    def _setup_layout(self) -> None:
        """Setup the main layout structure."""
        # Navigation layout for the button
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.original_button)
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

    def _add_preprocessing_widgets(self, layout: QVBoxLayout) -> None:
        """
        Add all preprocessing widgets to the layout.
        Args:
            layout (QVBoxLayout): The main layout to add widgets to
        """
        for name, widget_cls, controller in self.widget_data:
            widget = widget_cls(controller, self.event_bus)
            setattr(self, name, widget)
            layout.addWidget(widget)

    def _update_original_button_state(self) -> None:
        """
        Update the enabled state of the Original button based on whether
        the current column or whole dataset has been modified.
        """
        if not self.data_model:
            self.original_button.setEnabled(False)
            return
        
        whole_dataset = self.whole_dataset_checkbox.isChecked()
        
        if whole_dataset:
            is_modified = self.data_model.is_dataset_modified()
        else:
            is_modified = self.data_model.is_current_column_modified()
        
        self.original_button.setEnabled(is_modified)

    def _on_original_button_clicked(self) -> None:
        """Callback for original button"""
        whole_dataset = self.whole_dataset_checkbox.isChecked()
        self.event_bus.emit_type(
            EventType.DATA_REVERTED,
            whole_dataset
        )
        self._update_original_button_state()
        self._update_transformation_label()

    def _update_transformation_label(self) -> None:
        """Updates transformation_label"""
        text = self.data_model.current_transformation or "Original"
        self.transformation_label.setText(f"Current state: {text}")