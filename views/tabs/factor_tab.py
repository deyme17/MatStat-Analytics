import pandas as pd

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QPushButton, QComboBox,
    QRadioButton, QButtonGroup, QGroupBox, QScrollArea,
    QListWidget, QAbstractItemView,
)
from PyQt6.QtCore import Qt

from services import UIMessager
from utils import AppContext, EventBus, Event, EventType
from controllers import FactorController
from views.widgets import PFMResultWidget
from utils.ui_styles import groupMargin, groupStyle
from utils.helpers import create_section_header


MIN_FEATURES = 3
FEATURE_LIST_HEIGHT = 110
FEATURE_LIST_WIDTH = 310



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
        self.pfm_result_widget: PFMResultWidget = pfm_result_widget(self.context, 
                                                                    self.controller)
        self._init_ui()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_changed)

    def _on_data_changed(self, event: Event) -> None:
        """Refresh feature list and drop results computed on the previous data."""
        self._refresh_feature_list()
        self._on_clear()
        if self._is_pca_space():
            self._set_status(
                "Dataset is in PCA space. Restore original data in the PCA tab.", ok=False
            )

    def _init_ui(self) -> None:
        """Initializes unit interface if factor tab."""
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
        layout.addLayout(create_section_header("PFM Config"))
        layout.addWidget(self._build_feature_selector_group())
        layout.addWidget(self._build_params_group())
        layout.addWidget(self._init_h2_estimator_selector())
        layout.addWidget(self._build_actions_group())
        
        self.status_label = self._build_status_label()
        layout.addWidget(self.status_label)

        layout.addWidget(self.pfm_result_widget)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        self._refresh_buttons()

    def _build_feature_selector_group(self) -> QGroupBox:
        """Build group box with multi-select list for PFM feature selection."""
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
        """Build parameter group for PFM configuring."""
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

        n_label = QLabel("n_factors:")
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setMinimum(1)
        self.n_spinbox.setValue(2)
        self.n_spinbox.setFixedWidth(50)

        param_row.addWidget(n_label)
        param_row.addWidget(self.n_spinbox)
        param_row.addStretch()
        
        layout.addLayout(param_row)
        group.setLayout(layout)
        self._on_mode_toggled()
        return group

    def _init_h2_estimator_selector(self) -> QGroupBox:
        """Initialize communality estimator selection (QComboBox)"""
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
        """Build group of available actions."""
        box = QGroupBox("Actions")
        layout = QVBoxLayout()

        self.fit_btn = QPushButton("Fit Model")
        self.fit_btn.clicked.connect(self._on_fit)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self._on_clear)

        for btn in (self.fit_btn, self.clear_btn):
            btn.setFixedHeight(32)
            layout.addWidget(btn)

        box.setLayout(layout)
        return box

    def _build_status_label(self) -> QLabel:
        """Builds status label for something."""
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        label.setFixedHeight(30)
        label.setStyleSheet(
            "background:#ffffff; border:1px solid #ffffff; padding: 0 8px; border-radius:4px;"
        )
        return label
    
    # --- callbacks ---
    def _on_mode_toggled(self) -> None:
        """Toggle n_factors/auto radio button."""
        n_mode = self.radio_n.isChecked()
        self.n_spinbox.setEnabled(n_mode)

    def _on_feature_selection_changed(self) -> None:
        """Update label and cap n_spinbox maximum (n_factors must be < n_features)."""
        selected = self._get_selected_features()
        count = len(selected)
        self.selected_features_label.setText(f"Selected: {count} features")
        if count >= MIN_FEATURES:
            self.n_spinbox.setMaximum(count - 1)
        self._refresh_buttons()

    def _on_fit(self) -> None:
        """
        Fit Principal Factor Method model and find factor reflection.
        Call `pfm_result_widget.create_results` and set fit status.
        """
        data = self._get_data()
        if data is None: 
            return
        df, selected_cols = data
        if df is None: 
            return

        n_factors = self._get_n_factors()
        h2_estimator = self._get_h2_estimator()
        
        try:
            factor_reflection = self.controller.fit_transform(
                df[selected_cols], 
                h2_estimator_name=h2_estimator, 
                n_factors=n_factors,
            )
            self.pfm_result_widget.create_results(factor_reflection)
            self._set_fit_status()
        except Exception as e:
            self.messenger.show_error("Fit failed", str(e))

    def _on_clear(self) -> None:
        """Clear controller and widgets state."""
        self.controller.clear()
        self.pfm_result_widget.clear()
        self._set_status("Results cleared", ok=True)

    # --- helpers ---
    def _refresh_feature_list(self) -> None:
        """
        Repopulate QListWidget from VersionManager's current column registry.
        Rules:
        - In PCA space the list is empty and disabled (PFM needs original features).
        - If the columns did not change, the user's selection is kept.
        - If the columns changed, all of them are selected.
        """
        dataset_name = self.context.version_manager.get_current_dataset_name()
        columns = self.context.version_manager.get_all_columns_names(dataset_name)
        is_pca_space = self._is_pca_space()
        current = [self.feature_list.item(i).text() 
                   for i in range(self.feature_list.count())]

        self.feature_list.blockSignals(True)
        if is_pca_space:
            self.feature_list.clear()
        elif current != columns:
            self.feature_list.clear()
            for col in columns:
                self.feature_list.addItem(col)
            self.feature_list.selectAll()

        self.feature_list.setEnabled(not is_pca_space)
        self.select_all_btn.setEnabled(not is_pca_space)
        self.clear_sel_btn.setEnabled(not is_pca_space)

        self.feature_list.blockSignals(False)
        self._on_feature_selection_changed()

    def _is_pca_space(self) -> bool:
        """True if the current dataset holds PCA scores."""
        data_model = self.context.data_model
        return data_model.pca_state

    def _get_selected_features(self) -> list[str]:
        """Return list of currently selected feature names."""
        return [item.text() for item in self.feature_list.selectedItems()]

    def _select_all_features(self) -> None:
        """Select all items in feature list."""
        self.feature_list.selectAll()

    def _get_data(self) -> tuple[pd.DataFrame, list[str]] | None:
        """Return a DataFrame and user-selected features."""
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

            selected = self._get_selected_features()

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
        """Return the number of fctors if not 'auto'."""
        if self.radio_n.isChecked():
            return self.n_spinbox.value()
        return None

    def _get_h2_estimator(self) -> str:
        """Return list of names of available h2 estimators."""
        return self.h2_estimator_combo.currentText()

    def _refresh_buttons(self) -> None:
        """Enable/disable action buttons based on selection and data space."""
        enabled = (len(self._get_selected_features()) >= MIN_FEATURES and 
                   not self._is_pca_space())
        self.fit_btn.setEnabled(enabled)

    def _set_fit_status(self) -> None:
        """Show convergence status of the last fit."""
        res = self.controller.get_results()
        result, ok = res["result"], res["ok"]
        self._set_status(
            f"{result.value}, {res['n_iter']} iterations", ok=ok
        )

    def _set_status(self, msg: str, ok: bool = True) -> None:
        """Set status label to `msg` in color based `ok`."""
        color = "#e8f5e9" if ok else "#ffebee"
        border = "#a5d6a7" if ok else "#ef9a9a"
        self.status_label.setStyleSheet(
            f"background:{color}; border:1px solid {border}; padding: 0 8px; border-radius:4px;"
        )
        self.status_label.setText(msg)