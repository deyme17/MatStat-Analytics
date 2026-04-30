from typing import Optional, List, Tuple
import pandas as pd

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QPushButton,
    QRadioButton, QButtonGroup, QGroupBox, QScrollArea,
    QListWidget, QAbstractItemView,
)
from PyQt6.QtCore import Qt
from views.widgets.componentwidgets import PCAResultWidget

from services import UIMessager
from utils import AppContext, EventBus, Event, EventType
from services.ui_services.renderers.graph_renderers import ScreeEVRPlot
from controllers import ComponentController
from controllers.dp_controllers.component_controller import PCAState
from utils.ui_styles import groupMargin, groupStyle
from utils.helpers import create_section_header


MIN_FEATURES = 2
FEATURE_LIST_HEIGHT = 110
FEATURE_LIST_WIDTH = 310



class ComponentAnalysisTab(QWidget):
    """Component analysis tab that implements Principal Component Analysis."""
    def __init__(self, context: AppContext, 
                 component_controller: ComponentController,
                 pca_result_widget: type[PCAResultWidget]):
        """
        Args:
            context: Shared application context (data_model, event_bus, messager).
            component_controller: Controller for performing component analysis.
            pca_result_widget: Widget for displaying PCA result.
        """
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messenger: UIMessager = context.messanger
        self.controller: ComponentController = component_controller
        self.pca_result_widget: PCAResultWidget = pca_result_widget(self.context, 
                                                                    self.controller)
        self._init_ui()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)

    def _on_data_changed(self, event: Event) -> None:
        """Refresh feature list and button states whenever data changes."""
        self._refresh_feature_list()
        self._refresh_buttons()

    def _init_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container.setMaximumWidth(350)
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # build sections
        layout.addLayout(create_section_header("PCA Config"))
        layout.addWidget(self._build_feature_selector_group())
        layout.addWidget(self._build_params_group())
        layout.addWidget(self._build_actions_group())
        
        self.status_label = self._build_status_label()
        layout.addWidget(self.status_label)

        layout.addWidget(self.pca_result_widget)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        self._refresh_buttons()

    def _build_feature_selector_group(self) -> QGroupBox:
        """Build group box with multi-select list for PCA feature selection."""
        box = QGroupBox("Features (X)")
        layout = QVBoxLayout()

        self.feature_list = QListWidget()
        self.feature_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.feature_list.setMaximumHeight(FEATURE_LIST_HEIGHT)
        self.feature_list.setMaximumWidth(FEATURE_LIST_WIDTH)
        self.feature_list.itemSelectionChanged.connect(self._on_feature_selection_changed)

        # btns
        btn_row = QHBoxLayout()
        self.select_all_btn = QPushButton("Select ALL")
        self.clear_sel_btn = QPushButton("Clear selection")
        self.select_all_btn.clicked.connect(self._select_all_features)
        self.clear_sel_btn.clicked.connect(self.feature_list.clearSelection)
        btn_row.addWidget(self.select_all_btn)
        btn_row.addWidget(self.clear_sel_btn)

        self.selected_features_label = QLabel("Selected: 0 features")

        layout.addWidget(self.feature_list)
        layout.addLayout(btn_row)
        layout.addWidget(self.selected_features_label)
        box.setLayout(layout)
        return box

    def _build_params_group(self) -> QGroupBox:
        box = QGroupBox("Component Selection Mode")
        layout = QVBoxLayout()

        # selection mode
        radio_row = QHBoxLayout()
        self.radio_n = QRadioButton("Number of Components")
        self.radio_ev = QRadioButton("Variance Threshold")
        self.radio_n.setChecked(True)
        
        self._radio_group = QButtonGroup(self)
        self._radio_group.addButton(self.radio_n)
        self._radio_group.addButton(self.radio_ev)
        self._radio_group.buttonClicked.connect(self._on_mode_toggled)
        
        radio_row.addWidget(self.radio_n)
        radio_row.addWidget(self.radio_ev)
        radio_row.addStretch()
        layout.addLayout(radio_row)

        # parameters
        param_row = QHBoxLayout()

        n_label = QLabel("n_components:")
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setMinimum(1)
        self.n_spinbox.setValue(2)
        self.n_spinbox.setFixedWidth(50)

        ev_label = QLabel("ev_threshold:")
        self.ev_spinbox = QDoubleSpinBox()
        self.ev_spinbox.setRange(0.01, 1.0)
        self.ev_spinbox.setSingleStep(0.05)
        self.ev_spinbox.setValue(0.90)
        self.ev_spinbox.setDecimals(2)
        self.ev_spinbox.setFixedWidth(50)

        param_row.addWidget(n_label)
        param_row.addWidget(self.n_spinbox)
        param_row.addSpacing(20)
        param_row.addWidget(ev_label)
        param_row.addWidget(self.ev_spinbox)
        param_row.addStretch()
        
        layout.addLayout(param_row)
        box.setLayout(layout)
        self._on_mode_toggled()
        return box

    def _build_actions_group(self) -> QGroupBox:
        box = QGroupBox("Actions")
        layout = QVBoxLayout()

        self.fit_btn = QPushButton("Fit Model")
        self.fit_btn.clicked.connect(self._on_fit)

        self.transform_btn = QPushButton("Transform Data")
        self.transform_btn.clicked.connect(self._on_transform)

        self.scree_btn = QPushButton("Show Scree Plot")
        self.scree_btn.clicked.connect(self._on_scree_plot)

        self.inverse_btn = QPushButton("Inverse Transform (Reconstruct)")
        self.inverse_btn.clicked.connect(self._on_inverse_transform)

        self.original_btn = QPushButton("Restore Original Data")
        self.original_btn.clicked.connect(self._on_to_original)

        for btn in (self.fit_btn, self.transform_btn, self.scree_btn,
                    self.inverse_btn, self.original_btn):
            btn.setFixedHeight(32)
            layout.addWidget(btn)

        box.setLayout(layout)
        return box

    def _build_status_label(self) -> QLabel:
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        label.setFixedHeight(30)
        label.setStyleSheet(
            "background:#ffffff; border:1px solid #ffffff; padding: 0 8px; border-radius:4px;"
        )
        return label
    
    # --- callbacks ---
    def _on_mode_toggled(self) -> None:
        n_mode = self.radio_n.isChecked()
        self.n_spinbox.setEnabled(n_mode)
        self.ev_spinbox.setEnabled(not n_mode)

    def _on_feature_selection_changed(self) -> None:
        """Update label and cap n_spinbox maximum to number of selected features."""
        selected = self._get_selected_features()
        count = len(selected)
        self.selected_features_label.setText(f"Selected: {count} features")
        if count >= MIN_FEATURES:
            self.n_spinbox.setMaximum(count)

    def _on_fit(self) -> None:
        df, selected_cols = self._get_data()
        if df is None:
            return
        try:
            self.controller.fit(df[selected_cols])
            self.pca_result_widget.create_results()
            self._refresh_buttons()
            self._set_status("Model fitted successfully", ok=True)
        except Exception as e:
            self.messenger.show_error("Fit failed", str(e))

    def _on_transform(self) -> None:
        df, selected_cols = self._get_data()
        if df is None:
            return

        n_components, ev_threshold = self._get_params()
        state = self.controller.current_state
        current_dataset = self.context.version_manager.get_current_dataset_name()
        fit_needed = (state == PCAState.IDLE or 
                      self.controller.fitted_ds_name != current_dataset)
        try:
            self.controller.transform(df[selected_cols], df, fit_needed, n_components, ev_threshold)
            self.pca_result_widget.create_results()
            self._refresh_buttons()
            self._set_status(
                f"Transformed to {n_components or 'auto'} components", ok=True,
            )
        except Exception as e:
            self.messenger.show_error("Transform failed", str(e))

    def _on_scree_plot(self) -> None:
        try:
            _, evr = self.controller.get_explained_variance()
            dialog = ScreeEVRPlot(evr, parent=self)
            dialog.exec()
        except Exception as e:
            self.messenger.show_error("Scree plot failed", str(e))

    def _on_inverse_transform(self) -> None:
        df = self.context.data_model.dataframe
        if df is None:
            return
        try:
            self.controller.inverse_transform(df)
            self._refresh_buttons()
            self._set_status("Data inverse-transformed", ok=True)
        except Exception as e:
            self.messenger.show_error("Inverse transform failed", str(e))

    def _on_to_original(self) -> None:
        try:
            self.controller.to_original()
            self.pca_result_widget.refresh()
            self._refresh_buttons()
            self._set_status("Restored original data", ok=True)
        except Exception as e:
            self.messenger.show_error("Restore failed", str(e))

    # --- helpers ---
    def _refresh_feature_list(self) -> None:
        """
        Repopulate QListWidget from VersionManager's current column registry.
        Rules:
        - After PCA transform columns are PC_N - the list is disabled.
        - After dataset changed, the list is enabled and all columns are selected.
        """
        dataset_name = self.context.version_manager.get_current_dataset_name()
        columns = self.context.version_manager.get_all_columns_names(dataset_name)
        self.feature_list.blockSignals(True)
        self.feature_list.clear()

        is_pca_space = bool(columns) and all(c.startswith("PC_") for c in columns)
        if not is_pca_space:
            for col in columns:
                self.feature_list.addItem(col)
            self.feature_list.selectAll()

        self.feature_list.setEnabled(not is_pca_space)
        self.select_all_btn.setEnabled(not is_pca_space)
        self.clear_sel_btn.setEnabled(not is_pca_space)

        self.feature_list.blockSignals(False)
        self._on_feature_selection_changed()

    def _get_selected_features(self) -> list[str]:
        """Return list of currently selected feature names."""
        return [item.text() for item in self.feature_list.selectedItems()]

    def _select_all_features(self) -> None:
        self.feature_list.selectAll()

    def _get_data(self) -> Optional[Tuple[pd.DataFrame, List[str]]]:
        """Return a DataFrame and user-selected features."""
        try:
            df = self.context.data_model.dataframe
            if df is None or df.empty:
                self.messenger.show_error("Data Error", "No data loaded.")
                return None

            selected = self._get_selected_features()

            if len(selected) < MIN_FEATURES:
                self.messenger.show_error(
                    "Selection Error",
                    f"Please select at least {MIN_FEATURES} features for PCA."
                )
                return None

            missing = [c for c in selected if c not in df.columns]
            if missing:
                self.messenger.show_error(
                    "Selection Error",
                    f"Columns not found in current data: {', '.join(missing)}"
                )
                return None

            self.n_spinbox.setMaximum(len(selected))
            return df, selected

        except Exception as e:
            self.messenger.show_error("Data Read Error", str(e))
            return None

    def _get_params(self):
        if self.radio_n.isChecked():
            return self.n_spinbox.value(), None
        return None, self.ev_spinbox.value()

    def _refresh_buttons(self) -> None:
        """Enable/disable buttons based on current PCA state and active dataset."""
        state = self.controller.current_state
        current_dataset = self.context.version_manager.get_current_dataset_name()
        fitted_here = self.controller.fitted_ds_name == current_dataset
        has_enough_features = len(self._get_selected_features()) >= MIN_FEATURES

        self.fit_btn.setEnabled(has_enough_features and (state != PCAState.TRANSFORMED or not fitted_here))
        self.transform_btn.setEnabled(has_enough_features and (state != PCAState.TRANSFORMED or not fitted_here))
        self.scree_btn.setEnabled(state in (PCAState.FITTED, PCAState.TRANSFORMED) and fitted_here)
        self.original_btn.setEnabled(state == PCAState.TRANSFORMED and fitted_here)
        self.inverse_btn.setEnabled(state == PCAState.TRANSFORMED and fitted_here and 
                                    state != PCAState.INVERSE_TRANSFORMED)

    def _set_status(self, msg: str, ok: bool = True) -> None:
        color = "#e8f5e9" if ok else "#ffebee"
        border = "#a5d6a7" if ok else "#ef9a9a"
        self.status_label.setStyleSheet(
            f"background:{color}; border:1px solid {border}; padding: 0 8px; border-radius:4px;"
        )
        self.status_label.setText(msg)