from typing import Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QPushButton, QHBoxLayout, QGroupBox
)

from utils import EventBus, EventType, Event, AppContext
from controllers import DatasetController
from services import DataExporter, UIMessager, DataVersionManager
from views.widgets.utils import make_button, make_combo, make_checkbox

BUTTON_WIDTH, BUTTON_HEIGHT = 111, 30


class DataProcessingTab(QWidget):
    """
    A UI tab for managing data preprocessing steps including:
    - Data version selection
    - Transformations
    - Anomaly detection
    - Missing data handling
    - Original data restoration
    """
    def __init__(self, context: AppContext, 
                 data_exporter: DataExporter, 
                 dataset_controller: DatasetController, 
                 widget_data: list[tuple[str, QGroupBox, Any]]) -> None: 
        """
        Args:
            context: Shared application context (data_model, event_bus, messager).
            dataset_controller: Controller for handling dataset changes.
            data_exporter: Class for exporting data.
            widget_data (list[tuple[str, QGroupBox, Any]]): Widget classes for data 
                                        processing operations with it's controllers.
        """
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messanger: UIMessager = context.messanger
        self.version_manager: DataVersionManager = context.version_manager
        self.exporter: DataExporter = data_exporter
        self.dataset_controller: DatasetController = dataset_controller
        self.widget_data = widget_data

        self._init_ui()
        self._setup_layout()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        """Subscribe to data modification and navigation events."""
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_loaded)
        self.event_bus.subscribe(EventType.DATA_TRANSFORMED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.COLUMN_CHANGED, self._on_data_changed)

    def _on_data_loaded(self, event: Event) -> None:
        """Enable combo boxes when dataset is loaded."""
        dataset_count = len(self.context.version_manager.get_all_dataset_names())
        self.data_version_combo.setEnabled(dataset_count > 0)
        
        if self.context.data_model:
            col_count = self.context.data_model.dataframe.shape[1]
            self.dataframe_cols_combo.setEnabled(col_count > 0)
        
        self._update_button_state_on_data(self.original_button)
        self._update_button_state_on_data(self.export_button)
        self._update_transformation_label()

    def _on_data_changed(self, event: Event) -> None:
        """Refresh action buttons status and current state labels."""
        self._update_button_state_on_data(self.original_button)
        self._update_button_state_on_data(self.export_button)
        self._update_transformation_label()

    def _init_ui(self) -> None:
        """Initialize UI components."""
        self.data_version_label = QLabel("Select loaded dataset:")
        self.data_version_combo = make_combo(on_change=self.dataset_controller.on_dataset_selection_changed)
        self.transformation_label = QLabel("Current state: Original")

        self.current_col_label = QLabel("Select column to apply operation to:")
        self.dataframe_cols_combo = make_combo(on_change=self.dataset_controller.on_current_col_changed)
        
        self.whole_dataset_checkbox = make_checkbox("Whole dataset", checked=False, callback=self._on_checkbox_toggled)
        self.original_button = make_button("Original", callback=self._on_original_button_clicked, height=BUTTON_HEIGHT, width=BUTTON_WIDTH)
        self.export_button = make_button("Export Data", callback=self._on_export_data_clicked, height=BUTTON_HEIGHT, width=BUTTON_WIDTH)

    def _on_checkbox_toggled(self) -> None:
        """Update button state when whole dataset checkbox is toggled."""
        self._update_button_state_on_data(self.original_button)
        self._update_button_state_on_data(self.export_button)

    def _setup_layout(self) -> None:
        """Setup the main layout structure."""
        # navigation layout for the button
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.original_button)
        nav_layout.addWidget(self.export_button)
        nav_layout.addWidget(self.whole_dataset_checkbox)
        nav_layout.addStretch()

        # main layout
        layout = QVBoxLayout()
        layout.addWidget(self.data_version_label)
        layout.addWidget(self.data_version_combo)
        layout.addWidget(self.transformation_label)
        layout.addWidget(self.current_col_label)
        layout.addWidget(self.dataframe_cols_combo)

        # add preprocessing widgets
        self._add_preprocessing_widgets(layout)
        
        layout.addLayout(nav_layout)
        layout.addStretch()

        self.setLayout(layout)

    def _add_preprocessing_widgets(self, layout: QVBoxLayout) -> None:
        """Add all registered preprocessing widgets to layout."""
        for name, widget_cls, controller in self.widget_data:
            widget = widget_cls(controller, self.event_bus)
            setattr(self, name, widget)
            layout.addWidget(widget)

    def _update_button_state_on_data(self, button: QPushButton) -> None:
        """Update button status based on dataset modification state."""
        if not self.context.data_model:
            button.setEnabled(False)
            return
        
        whole_dataset = self.whole_dataset_checkbox.isChecked()
        is_modified = (
            self.context.data_model.is_dataset_modified() 
            if whole_dataset 
            else self.context.data_model.is_current_column_modified()
        )
        button.setEnabled(is_modified)

    def _on_original_button_clicked(self) -> None:
        """Callback for reverting to original dataset/column state."""
        whole_dataset = self.whole_dataset_checkbox.isChecked()
        self.dataset_controller.revert_to_original(whole_dataset)

    def _update_transformation_label(self) -> None:
        """Update label indicating active data transformation."""
        if not self.context.data_model:
            self.transformation_label.setText("Current state: No Data")
            return
        text = self.context.data_model.current_transformation or "Original"
        self.transformation_label.setText(f"Current state: {text}")

    def _on_export_data_clicked(self) -> None:
        """Callback for exporting selected data slice to disk."""
        curr_data = self.context.data_model
        if not curr_data:
            self.messanger.show_error("No data available for export.")
            return
        
        whole_dataset = self.whole_dataset_checkbox.isChecked()

        try:
            if whole_dataset and curr_data.dataframe is not None:
                export_data = curr_data.dataframe
                name = f"{self.version_manager.get_current_dataset_name()}"
            elif curr_data.series is not None:
                export_data = curr_data.series.to_numpy()
                name = f"{self.version_manager.get_current_dataset_name()}_col{self.version_manager.get_current_column_name()}"
            else:
                self.messanger.show_error("Export error", "No data to export.")
                return

            filepath = self.exporter.export(name, export_data, out_dir="data/exported_data")
            self.messanger.show_info("Data Export", f"Data exported successfully to:\n{filepath}")

        except Exception as e:
            self.messanger.show_error("Export error", f"Export failed: {e}")