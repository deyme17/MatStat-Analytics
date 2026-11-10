import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QRadioButton, 
    QButtonGroup, QGroupBox, QScrollArea,
)
from PyQt6.QtCore import Qt

from views.widgets.componentwidgets import PCAResultWidget
from views.widgets.utils.common_widgets import FeatureSelectorWidget
from services import UIMessager
from utils import AppContext, EventBus, Event, EventType
from services.ui_services.renderers.graph_renderers import ScreeEVRPlot
from controllers import ComponentController
from controllers.analysis_controllers.component_controller import PCAState
from views.widgets.utils import (
    create_section_header, create_status_label, update_status_label, make_button
)
from utils.ui_styles import groupMargin, groupStyle


MIN_FEATURES = 2


class ComponentTab(QWidget):
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
        self.pca_result_widget: PCAResultWidget = pca_result_widget(self.context, self.controller)
        
        self._init_ui()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        """Subscribe controller to EventBus events."""
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_reverted)

    def _on_data_changed(self, event: Event) -> None:
        """Refresh feature list and button states whenever data changes."""
        self._refresh_feature_list()
        self._refresh_buttons()

    def _on_data_reverted(self, event: Event) -> None:
        """Clear PCA results, refresh UI state, and reset PCA flag in DataModel."""
        self.pca_result_widget.clear()
        self._on_data_changed(event)
        self.context.data_model.set_pca_space(False)
        update_status_label(self.status_label, "Data reverted to original", ok=True)

    def _init_ui(self) -> None:
        """Initialize user interface layout of component tab."""
        main_layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container.setMaximumWidth(350)
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Build UI sections
        layout.addLayout(create_section_header("PCA Config"))
        
        self.feature_selector = FeatureSelectorWidget(title="Features (X)", label_prefix="features")
        self.feature_selector.list_widget.itemSelectionChanged.connect(self._on_feature_selection_changed)
        layout.addWidget(self.feature_selector)

        layout.addWidget(self._build_params_group())
        layout.addWidget(self._build_actions_group())
        
        self.status_label = create_status_label()
        layout.addWidget(self.status_label)

        layout.addWidget(self.pca_result_widget)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        self._refresh_buttons()

    def _build_params_group(self) -> QGroupBox:
        """Build parameter group for PCA configuration."""
        box = QGroupBox("Component Selection Mode")
        layout = QVBoxLayout()

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

        param_row = QHBoxLayout()
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setMinimum(1)
        self.n_spinbox.setValue(2)
        self.n_spinbox.setFixedWidth(50)

        self.ev_spinbox = QDoubleSpinBox()
        self.ev_spinbox.setRange(0.01, 1.0)
        self.ev_spinbox.setSingleStep(0.05)
        self.ev_spinbox.setValue(0.90)
        self.ev_spinbox.setDecimals(2)
        self.ev_spinbox.setFixedWidth(50)

        param_row.addWidget(QLabel("n_components:"))
        param_row.addWidget(self.n_spinbox)
        param_row.addSpacing(20)
        param_row.addWidget(QLabel("ev_threshold:"))
        param_row.addWidget(self.ev_spinbox)
        param_row.addStretch()
        
        layout.addLayout(param_row)
        box.setLayout(layout)
        self._on_mode_toggled()
        return box

    def _build_actions_group(self) -> QGroupBox:
        """Build group of available action buttons."""
        box = QGroupBox("Actions")
        layout = QVBoxLayout()

        self.fit_btn = make_button("Fit Model", callback=self._on_fit, height=32)
        self.transform_btn = make_button("Transform Data", callback=self._on_transform, height=32)
        self.scree_btn = make_button("Show Scree Plot", callback=self._on_scree_plot, height=32)
        self.inverse_btn = make_button("Inverse Transform (Reconstruct)", callback=self._on_inverse_transform, height=32)
        self.original_btn = make_button("Restore Original Data", callback=self._on_to_original, height=32)

        for btn in (self.fit_btn, self.transform_btn, self.scree_btn, self.inverse_btn, self.original_btn):
            layout.addWidget(btn)

        box.setLayout(layout)
        return box

    # --- callbacks ---

    def _on_mode_toggled(self) -> None:
        """Toggle spinbox controls based on selection mode."""
        n_mode = self.radio_n.isChecked()
        self.n_spinbox.setEnabled(n_mode)
        self.ev_spinbox.setEnabled(not n_mode)

    def _on_feature_selection_changed(self) -> None:
        """Update label and restrict max n_components based on selected feature count."""
        self.feature_selector.update_count_label()
        count = len(self.feature_selector.get_selected_items())
        if count >= MIN_FEATURES:
            self.n_spinbox.setMaximum(count)

    def _on_fit(self) -> None:
        """Fit Principal Component Analysis model on selected features."""
        data = self._get_data()
        if data is None: 
            return
        df, selected_cols = data
        
        try:
            self.controller.fit(df[selected_cols])
            self.pca_result_widget.create_results()
            self._refresh_buttons()
            update_status_label(self.status_label, "Model fitted successfully", ok=True)
        except Exception as e:
            self.messenger.show_error("Fit failed", str(e))

    def _on_transform(self) -> None:
        """Transform dataset using fitted PCA model."""
        data = self._get_data()
        if data is None: 
            return
        df, selected_cols = data

        n_components, ev_threshold = self._get_params()
        state = self.controller.current_state
        current_dataset = self.context.version_manager.get_current_dataset_name()
        fit_needed = (state == PCAState.IDLE or self.controller.fitted_ds_name != current_dataset)

        try:
            self.controller.transform(df[selected_cols], df, fit_needed, n_components, ev_threshold)
            self.context.data_model.set_pca_space(True)
            self.pca_result_widget.create_results()
            self._refresh_buttons()
            update_status_label(self.status_label, f"Transformed to {n_components or 'auto'} components", ok=True)
        except Exception as e:
            self.messenger.show_error("Transform failed", str(e))

    def _on_scree_plot(self) -> None:
        """Open Scree Plot visualization dialog."""
        try:
            _, evr = self.controller.get_explained_variance()
            dialog = ScreeEVRPlot(evr, parent=self)
            dialog.exec()
        except Exception as e:
            self.messenger.show_error("Scree plot failed", str(e))

    def _on_inverse_transform(self) -> None:
        """Apply inverse transform to reconstructed space."""
        df = self.context.data_model.dataframe
        if df is None:
            return
        try:
            self.controller.inverse_transform(df)
            self.context.data_model.set_pca_space(False)
            self._refresh_buttons()
            update_status_label(self.status_label, "Data inverse-transformed", ok=True)
        except Exception as e:
            self.messenger.show_error("Inverse transform failed", str(e))

    def _on_to_original(self) -> None:
        """Revert data to original feature space."""
        try:
            self.controller.to_original()
            self.context.data_model.set_pca_space(False)
            self.pca_result_widget.refresh()
            self._refresh_buttons()
            update_status_label(self.status_label, "Restored original data", ok=True)
        except Exception as e:
            self.messenger.show_error("Restore failed", str(e))

    # --- helpers ---

    def _refresh_feature_list(self) -> None:
        """Repopulate feature selection list from column registry."""
        dataset_name = self.context.version_manager.get_current_dataset_name()
        columns = self.context.version_manager.get_all_columns_names(dataset_name)
        is_pca_space = self.context.data_model.pca_space

        if not is_pca_space:
            self.feature_selector.populate(columns, select_all=True)
        else:
            self.feature_selector.list_widget.clear()

        self.feature_selector.set_enabled_state(not is_pca_space)
        self._on_feature_selection_changed()

    def _get_data(self) -> tuple[pd.DataFrame, list[str]] | None:
        """Retrieve active dataframe and verified feature selection list."""
        try:
            df = self.context.data_model.dataframe
            if df is None or df.empty:
                self.messenger.show_error("Data Error", "No data loaded.")
                return None

            selected = self.feature_selector.get_selected_items()
            if len(selected) < MIN_FEATURES:
                self.messenger.show_error("Selection Error", f"Please select at least {MIN_FEATURES} features for PCA.")
                return None

            missing = [c for c in selected if c not in df.columns]
            if missing:
                self.messenger.show_error("Selection Error", f"Columns not found in current data: {', '.join(missing)}")
                return None

            self.n_spinbox.setMaximum(len(selected))
            return df, selected
        except Exception as e:
            self.messenger.show_error("Data Read Error", str(e))
            return None

    def _get_params(self) -> tuple[int | None, float | None]:
        """Return parameters configuration based on active radio mode."""
        if self.radio_n.isChecked():
            return self.n_spinbox.value(), None
        return None, self.ev_spinbox.value()

    def _refresh_buttons(self) -> None:
        """Update interactive buttons enablement depending on current PCA state."""
        state = self.controller.current_state
        current_dataset = self.context.version_manager.get_current_dataset_name()
        fitted_here = self.controller.fitted_ds_name == current_dataset
        has_enough_features = len(self.feature_selector.get_selected_items()) >= MIN_FEATURES

        self.fit_btn.setEnabled(has_enough_features and (state != PCAState.TRANSFORMED or not fitted_here))
        self.transform_btn.setEnabled(has_enough_features and (state != PCAState.TRANSFORMED or not fitted_here))
        self.scree_btn.setEnabled(state in (PCAState.FITTED, PCAState.TRANSFORMED) and fitted_here)
        self.original_btn.setEnabled(state == PCAState.TRANSFORMED and fitted_here)
        self.inverse_btn.setEnabled(state == PCAState.TRANSFORMED and fitted_here and state != PCAState.INVERSE_TRANSFORMED)