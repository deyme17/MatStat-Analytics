import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt

from views.widgets.utils.common_widgets import FeatureSelectorWidget
from views.widgets.utils import create_section_header, create_status_label
from utils.ui_styles import groupMargin, groupStyle
from utils import AppContext, EventBus, Event, EventType
from services import UIMessager


class BaseAnalysisTab(QWidget):
    """Base analysis tab providing common layout, feature selection, and data validation."""
    def __init__(self, context: AppContext, title: str):
        """
        Args:
            context: Shared application context (data_model, event_bus, messager).
            title: Title text for the section header.
        """
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messenger: UIMessager = context.messanger

        self._init_base_ui(title)
        self._subscribe_base_events()

    def _subscribe_base_events(self) -> None:
        """Subscribe base tab to Data events."""
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_changed)

    def _init_base_ui(self, title: str) -> None:
        """Initialize basic layout structure and feature selector."""
        main_layout = QVBoxLayout(self)

        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container.setMaximumWidth(350)
        self.layout = QVBoxLayout(container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.layout.addLayout(create_section_header(title))

        self.feature_selector = FeatureSelectorWidget(title="Features (X)", label_prefix="features")
        self.feature_selector.list_widget.itemSelectionChanged.connect(self._on_feature_selection_changed)
        self.layout.addWidget(self.feature_selector)

        self._build_custom_ui()

        self.status_label = create_status_label()
        self.layout.addWidget(self.status_label)

        self._build_result_widget()
        self.layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setWidget(container)

        main_layout.addWidget(scroll)

    def _build_custom_ui(self) -> None:
        """Override in subclasses to insert params and actions widgets."""
        pass

    def _build_result_widget(self) -> None:
        """Override in subclasses to build specific result widget."""
        pass

    def _on_feature_selection_changed(self) -> None:
        """Update feature count label. Override in subclasses for extra bounds checking."""
        self.feature_selector.update_count_label()

    def _on_data_changed(self, event: Event) -> None:
        """Refresh feature list on dataset modifications."""
        self._refresh_feature_list()

    def _is_pca_space(self) -> bool:
        """Check if current dataset state is in PCA space."""
        return self.context.data_model is not None and self.context.data_model.pca_space

    def _refresh_feature_list(self) -> None:
        """Repopulate feature selector items depending on dataset space."""
        dataset_name = self.context.version_manager.get_current_dataset_name()
        columns = self.context.version_manager.get_all_columns_names(dataset_name)
        is_pca_space = self._is_pca_space()

        if is_pca_space:
            self.feature_selector.list_widget.clear()
        else:
            self.feature_selector.populate(columns, select_all=True)

        self.feature_selector.set_enabled_state(not is_pca_space)
        self._on_feature_selection_changed()

    def _get_data(self, min_features: int) -> tuple[pd.DataFrame, list[str]] | None:
        """Retrieve active dataframe and verified feature selection list."""
        try:
            df = self.context.data_model.dataframe
            if df is None or df.empty:
                self.messenger.show_error("Data Error", "No data loaded.")
                return None

            if self._is_pca_space():
                self.messenger.show_error(
                    "Data Error",
                    "Dataset is in PCA space. Restore original data in the PCA tab."
                )
                return None

            selected = self.feature_selector.get_selected_items()
            if len(selected) < min_features:
                self.messenger.show_error(
                    "Selection Error",
                    f"Please select at least {min_features} features."
                )
                return None

            missing = [c for c in selected if c not in df.columns]
            if missing:
                self.messenger.show_error(
                    "Selection Error",
                    f"Columns not found in current data: {', '.join(missing)}"
                )
                return None

            return df, selected
        except Exception as e:
            self.messenger.show_error("Data Read Error", str(e))
            return None