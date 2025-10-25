from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QGroupBox, QCheckBox
from typing import Any
from utils import EventBus, EventType, Event, AppContext
from controllers import DataVersionController

BUTTON_WIDTH, BUTTON_HEIGHT = 222, 30


class DataProcessingTab(QWidget):
    """
    A UI tab for managing data preprocessing steps including:
    - Data version selection
    - Transformations
    - Anomaly detection
    - Missing data handling
    - Original data restoration
    """
    def __init__(self, context: AppContext, data_version_controller: DataVersionController, widget_data: list[tuple[str, QGroupBox, Any]]):
        """
        Args:
            context: Shared application context (version_manager, event_bus, messager)
            data_version_controller: Controller for handling data version changes
            widget_data (list[tuple[str, QGroupBox, Any]]): Widget classes for data processing operations with it's controllers
        """
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.data_version_controller: DataVersionController = data_version_controller
        self.widget_data = widget_data

        self._init_ui()
        self._setup_layout()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_loaded)
        self.event_bus.subscribe(EventType.DATA_TRANSFORMED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.COLUMN_CHANGED, self._on_data_changed)

    def _on_data_loaded(self, event: Event) -> None:
        """Enable combo boxes when data is loaded"""
        dataset_count = len(self.context.version_manager.get_all_dataset_names())
        self.data_version_combo.setEnabled(dataset_count > 0)
        
        if self.context.data_model:
            col_count = self.context.data_model.dataframe.shape[1]
            self.dataframe_cols_combo.setEnabled(col_count > 0)
        
        self._update_original_button_state()
        self._update_transformation_label()

    def _on_data_changed(self, event: Event) -> None:
        self._update_original_button_state()
        self._update_transformation_label()

    def _init_ui(self) -> None:
        """Initialize UI components."""
        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = QComboBox()
        self.data_version_combo.setEnabled(False)
        self.data_version_combo.currentIndexChanged.connect(self.data_version_controller.on_dataset_selection_changed)

        self.transformation_label = QLabel("Current state: Original")

        self.current_col_label = QLabel("Select column to apply operation to: ")
        self.dataframe_cols_combo = QComboBox()
        self.dataframe_cols_combo.setEnabled(False)
        self.dataframe_cols_combo.currentIndexChanged.connect(self.data_version_controller.on_current_col_changed)

        self.whole_dataset_checkbox = QCheckBox("Whole dataset")
        self.whole_dataset_checkbox.setChecked(False)
        self.whole_dataset_checkbox.toggled.connect(self._on_checkbox_toggled)

        self.original_button = QPushButton("Original")
        self.original_button.setEnabled(False)
        self.original_button.setFixedSize(BUTTON_WIDTH // 2, BUTTON_HEIGHT)
        self.original_button.clicked.connect(self._on_original_button_clicked)

        self.export_button = QPushButton("Export Data")
        self.export_button.setEnabled(False)
        self.export_button.setFixedSize(BUTTON_WIDTH // 2, BUTTON_HEIGHT)
        self.export_button.clicked.connect(lambda: None)

    def _on_checkbox_toggled(self) -> None:
        """Update button state when checkbox is toggled"""
        self._update_original_button_state()

    def _setup_layout(self) -> None:
        """Setup the main layout structure."""
        # Navigation layout for the button
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.original_button)
        nav_layout.addWidget(self.export_button)
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
        if not self.context.data_model:
            self.original_button.setEnabled(False)
            return
        
        whole_dataset = self.whole_dataset_checkbox.isChecked()
        
        if whole_dataset:
            is_modified = self.context.data_model.is_dataset_modified()
        else:
            is_modified = self.context.data_model.is_current_column_modified()
        
        self.original_button.setEnabled(is_modified)

    def _on_original_button_clicked(self) -> None:
        """Callback for original button - directly calls controller"""
        whole_dataset = self.whole_dataset_checkbox.isChecked()
        self.data_version_controller.revert_to_original(whole_dataset)

    def _update_transformation_label(self) -> None:
        """Updates transformation_label"""
        if not self.context.data_model:
            self.transformation_label.setText("Current state: No Data")
            return
        text = self.context.data_model.current_transformation or "Original"
        self.transformation_label.setText(f"Current state: {text}")