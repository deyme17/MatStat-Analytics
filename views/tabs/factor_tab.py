import pandas as pd

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QComboBox, QRadioButton, QButtonGroup, 
    QGroupBox, QScrollArea,
)
from PyQt6.QtCore import Qt

from services import UIMessager
from utils import AppContext, EventBus, Event, EventType
from controllers import FactorController
from views.widgets.factorwidgets import PFMResultWidget
from views.widgets.utils.common_widgets import FeatureSelectorWidget
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import (
    create_section_header, create_status_label, update_status_label, make_button
)


MIN_FEATURES = 3


class FactorTab(QWidget):
    """Factor analysis tab that implements Principal Factor Analysis."""
    def __init__(self, context: AppContext, 
                 factor_controller: FactorController,
                 pfm_result_widget: type[PFMResultWidget]):
        """
        Args:
            context: Shared application context (data_model, event_bus, messager).
            factor_controller: Controller for performing factor analysis.
            pfm_result_widget: Widget for displaying PFM result.
        """
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messenger: UIMessager = context.messanger
        self.controller: FactorController = factor_controller
        self.pfm_result_widget: PFMResultWidget = pfm_result_widget(self.context, self.controller)
        
        self._init_ui()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        """Subscribe to Data events."""
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_changed)

    def _on_data_changed(self, event: Event) -> None:
        """Refresh feature list and clear stale factor analysis results."""
        self._refresh_feature_list()
        self._on_clear()
        if self._is_pca_space():
            update_status_label(
                self.status_label, 
                "Dataset is in PCA space. Restore original data in the PCA tab.", 
                ok=False
            )

    def _init_ui(self) -> None:
        """Initializes user interface layout of factor tab."""
        main_layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container.setMaximumWidth(350)
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # build ui sections
        layout.addLayout(create_section_header("PFM Config"))
        
        self.feature_selector = FeatureSelectorWidget(title="Features (X)", label_prefix="features")
        self.feature_selector.list_widget.itemSelectionChanged.connect(self._on_feature_selection_changed)
        layout.addWidget(self.feature_selector)

        layout.addWidget(self._build_params_group())
        layout.addWidget(self._init_h2_estimator_selector())
        layout.addWidget(self._build_actions_group())
        
        self.status_label = create_status_label()
        layout.addWidget(self.status_label)

        layout.addWidget(self.pfm_result_widget)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        self._refresh_buttons()

    def _build_params_group(self) -> QGroupBox:
        """Build parameter group for PFM configuration."""
        group = QGroupBox("Factor Selection Mode")
        layout = QVBoxLayout()

        # selection mode
        radio_row = QHBoxLayout()
        self.radio_n = QRadioButton("Number of Factors")
        self.radio_auto = QRadioButton("Auto")
        self.radio_auto.setChecked(True)
        
        self._radio_group = QButtonGroup(self)
        self._radio_group.addButton(self.radio_n)
        self._radio_group.addButton(self.radio_auto)
        self._radio_group.buttonClicked.connect(self._on_mode_toggled)
        
        radio_row.addWidget(self.radio_n)
        radio_row.addWidget(self.radio_auto)
        radio_row.addStretch()
        layout.addLayout(radio_row)

        # parameters
        param_row = QHBoxLayout()
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setMinimum(1)
        self.n_spinbox.setValue(2)
        self.n_spinbox.setFixedWidth(50)

        param_row.addWidget(QLabel("n_factors:"))
        param_row.addWidget(self.n_spinbox)
        param_row.addStretch()
        
        layout.addLayout(param_row)
        group.setLayout(layout)
        self._on_mode_toggled()
        return group

    def _init_h2_estimator_selector(self) -> QGroupBox:
        """Initialize communality estimator selection combobox."""
        group = QGroupBox("Communality Estimator Selection")
        group_layout = QVBoxLayout()
        
        self.h2_estimator_combo = QComboBox()
        for method in self.controller.get_h2_estimators_names():
            self.h2_estimator_combo.addItem(method)
        
        group_layout.addWidget(QLabel("h^2 Estimators:"))
        group_layout.addWidget(self.h2_estimator_combo)
        group.setLayout(group_layout)
        return group

    def _build_actions_group(self) -> QGroupBox:
        """Build actions control group."""
        box = QGroupBox("Actions")
        layout = QVBoxLayout()

        self.fit_btn = make_button("Fit Model", callback=self._on_fit, height=32)
        self.clear_btn = make_button("Clear", callback=self._on_clear, height=32)

        layout.addWidget(self.fit_btn)
        layout.addWidget(self.clear_btn)

        box.setLayout(layout)
        return box

    # --- callbacks ---

    def _on_mode_toggled(self) -> None:
        """Toggle spinbox state based on radio button choice."""
        n_mode = self.radio_n.isChecked()
        self.n_spinbox.setEnabled(n_mode)

    def _on_feature_selection_changed(self) -> None:
        """Update label and restrict maximum allowed factors."""
        self.feature_selector.update_count_label()
        count = len(self.feature_selector.get_selected_items())
        if count >= MIN_FEATURES:
            self.n_spinbox.setMaximum(count - 1)
        self._refresh_buttons()

    def _on_fit(self) -> None:
        """Fit Principal Factor Method model."""
        data = self._get_data()
        if data is None: 
            return
        df, selected_cols = data

        n_factors = self._get_n_factors()
        h2_estimator = self._get_h2_estimator()
        
        try:
            self.controller.fit_transform(
                df[selected_cols], 
                h2_estimator_name=h2_estimator, 
                n_factors=n_factors,
            )
            self.pfm_result_widget.create_results()
            self._set_fit_status()
        except Exception as e:
            self.messenger.show_error("Fit failed", str(e))

    def _on_clear(self) -> None:
        """Clear controller state and PFM widget results."""
        self.controller.clear()
        self.pfm_result_widget.clear()
        update_status_label(self.status_label, "Results cleared", ok=True)

    # --- helpers ---

    def _refresh_feature_list(self) -> None:
        """Repopulate feature selector items depending on dataset space."""
        dataset_name = self.context.version_manager.get_current_dataset_name()
        columns = self.context.version_manager.get_all_columns_names(dataset_name)
        is_pca_space = self._is_pca_space()
        
        current = [self.feature_selector.list_widget.item(i).text() 
                   for i in range(self.feature_selector.list_widget.count())]

        if is_pca_space:
            self.feature_selector.list_widget.clear()
        elif current != columns:
            self.feature_selector.populate(columns, select_all=True)

        self.feature_selector.set_enabled_state(not is_pca_space)
        self._on_feature_selection_changed()

    def _is_pca_space(self) -> bool:
        """Check if current dataset state is in PCA space."""
        return self.context.data_model.pca_space

    def _get_data(self) -> tuple[pd.DataFrame, list[str]] | None:
        """Get dataframe and selected columns for calculation."""
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
            if len(selected) < MIN_FEATURES:
                self.messenger.show_error(
                    "Selection Error",
                    f"Please select at least {MIN_FEATURES} features for PFM."
                )
                return None

            missing = [c for c in selected if c not in df.columns]
            if missing:
                self.messenger.show_error(
                    "Selection Error",
                    f"Columns not found in current data: {', '.join(missing)}"
                )
                return None

            self.n_spinbox.setMaximum(len(selected) - 1)
            return df, selected
        except Exception as e:
            self.messenger.show_error("Data Read Error", str(e))
            return None

    def _get_n_factors(self) -> int | None:
        """Return selected number of factors or None if Auto mode."""
        if self.radio_n.isChecked():
            return self.n_spinbox.value()
        return None

    def _get_h2_estimator(self) -> str:
        """Return currently selected communality estimator method name."""
        return self.h2_estimator_combo.currentText()

    def _refresh_buttons(self) -> None:
        """Refresh actions buttons enablement."""
        enabled = (len(self.feature_selector.get_selected_items()) >= MIN_FEATURES and not self._is_pca_space())
        self.fit_btn.setEnabled(enabled)

    def _set_fit_status(self) -> None:
        """Display status of model convergence."""
        res = self.controller.get_results()
        result, ok = res["result"], res["ok"]
        update_status_label(
            self.status_label, 
            f"{result.value}, {res['n_iter']} iterations", 
            ok=ok
        )