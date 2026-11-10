from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QGroupBox, QLabel, QDoubleSpinBox, QScrollArea
)
from PyQt6.QtCore import Qt

from views.widgets.regressionwidgets import RegrSummaryWidget, RegrPredictionWidget
from views.widgets.utils.common_widgets import FeatureSelectorWidget
from utils import AppContext, EventBus, EventType, Event
from services import UIMessager
from controllers import RegressionController
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import make_button


LIST_WIDGET_HEIGHT = 100
LIST_WIDGET_WIDTH = 330
MAX_GROUP_HEIGHT = 150

ALPHA_MIN, ALPHA_MAX = 0.01, 0.99
ALPHA_STEP = 0.01
ALPHA_PRECISION = 2
DEFAULT_ALPHA = 0.05


class RegressionTab(QWidget):
    """Tab for conducting regression analysis."""
    def __init__(self, context: AppContext, 
                 regr_controller: RegressionController,
                 summary_widget: type[RegrSummaryWidget], 
                 prediction_widget: type[RegrPredictionWidget]):
        """
        Args:
            context: AppContext with data_model, event_bus and messenger
            regr_controller: controller for performing regression steps (fitting -> evaluating -> prediction)
            summary_widget: Widget for model post-fit summury (R^2, std.err., CI, etc.)
            prediction_widget: Widget for making predictions for new data using fitted model
        """
        super().__init__()
        self.context: AppContext = context
        self.messenger: UIMessager = context.messanger
        self.event_bus: EventBus = context.event_bus
        self.controller: RegressionController = regr_controller

        self.summary_widget: RegrSummaryWidget = summary_widget(self.context, self.controller)
        self.prediction_widget: RegrPredictionWidget = prediction_widget(self.context, self.controller)

        self._init_ui()
        self._connect_signals()
        self._subscribe_to_events()
        self._refresh_data()

    def _subscribe_to_events(self) -> None:
        """Subscribe to event bus events."""
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)

    def _on_data_changed(self, event: Event) -> None:
        """Handle data changed event."""
        self._refresh_data()

    def _init_ui(self) -> None:
        """Initialize and layout all UI components."""
        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container_layout = QVBoxLayout()
        
        self._init_model_selector(container_layout)
        
        self.independent_selector = FeatureSelectorWidget(
            title="Independent Variables (X)", 
            label_prefix="variables", 
            height=LIST_WIDGET_HEIGHT, 
            width=LIST_WIDGET_WIDTH
        )
        self.independent_selector.setMaximumHeight(MAX_GROUP_HEIGHT)
        container_layout.addWidget(self.independent_selector)

        self._init_dependent_var_selector(container_layout)
        
        self.fit_btn = make_button("Fit the model", callback=self._fit_model)
        container_layout.addWidget(self.fit_btn)
        
        self._init_alpha_controls(container_layout)
        container_layout.addWidget(self.summary_widget)
        container_layout.addWidget(self.prediction_widget)
        
        container_layout.addStretch()
        container.setLayout(container_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def _init_alpha_controls(self, layout: QVBoxLayout) -> None:
        """Initialize significance level controls."""
        self.alpha_spinbox = QDoubleSpinBox()
        self.alpha_spinbox.setRange(ALPHA_MIN, ALPHA_MAX)
        self.alpha_spinbox.setSingleStep(ALPHA_STEP)
        self.alpha_spinbox.setDecimals(ALPHA_PRECISION)
        self.alpha_spinbox.setValue(DEFAULT_ALPHA)
        self.alpha_spinbox.valueChanged.connect(self._on_alpha_changed)

        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Significance level α:"))
        alpha_layout.addWidget(self.alpha_spinbox)
        alpha_layout.addStretch()

        layout.addLayout(alpha_layout)

    def _init_model_selector(self, layout: QVBoxLayout) -> None:
        """Initialize model selection combobox."""
        group = QGroupBox("Model Selection")
        group_layout = QVBoxLayout()
        
        self.model_combo = QComboBox()
        for model_name in self.controller.regression_models:
            self.model_combo.addItem(model_name)
        
        group_layout.addWidget(QLabel("Regression model:"))
        group_layout.addWidget(self.model_combo)
        group.setLayout(group_layout)
        layout.addWidget(group)

    def _init_dependent_var_selector(self, layout: QVBoxLayout) -> None:
        """Initialize dependent variable selection combobox."""
        group = QGroupBox("Dependent Variable (Y)")
        group_layout = QVBoxLayout()
        
        self.dependent_combo = QComboBox()
        group_layout.addWidget(QLabel("Target variable:"))
        group_layout.addWidget(self.dependent_combo)
        group.setLayout(group_layout)
        layout.addWidget(group)

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        self.independent_selector.list_widget.itemSelectionChanged.connect(
            self.independent_selector.update_count_label
        )

    def _on_alpha_changed(self) -> None:
        """Handle alpha spinbox change."""
        alpha = self.alpha_spinbox.value()
        self.summary_widget.create_summary(alpha)
        self.prediction_widget.set_alpha_value(alpha)

    def _refresh_data(self) -> None:
        """Refresh available datasets and feature options."""
        self.independent_selector.list_widget.clear()
        self.dependent_combo.clear()
        
        data_model = self.context.data_model
        if data_model is None: 
            return
        df = data_model.dataframe
        if df.empty: 
            return

        columns = sorted(list(set(df.columns)))
        self.independent_selector.populate(columns, select_all=False)
        
        for col in columns:
            self.dependent_combo.addItem(col)

        if self.dependent_combo.count() > 0:
            self.dependent_combo.setCurrentIndex(self.dependent_combo.count() - 1)

    def _fit_model(self) -> None:
        """Fit a selected regression model."""
        if not self._validate_configuration():
            return
        self.summary_widget.clear()
        self.prediction_widget.clear()

        try:
            model_name = self.model_combo.currentText()
            x_vars = self.independent_selector.get_selected_items()
            y_var = self.dependent_combo.currentText()
            
            # get data
            data_model = self.context.data_model
            if data_model is None: 
                return
            df = data_model.dataframe
            if df.empty: 
                return
            
            # check if all columns exist
            missing_cols = [col for col in x_vars + [y_var] if col not in df.columns]
            if missing_cols:
                self.messenger.show_error("Fitting error", f"Missing columns: {', '.join(missing_cols)}")
                return
            
            # data preperation
            X_df = df[x_vars]
            y_series = df[y_var]
            
            # fit model
            self.controller.fit(model_name, X_df, y_series)
            
            # update widgets
            self.summary_widget.create_summary()
            self.prediction_widget.setup_for_model(x_vars)
            
            self.messenger.show_info(
                "Success", 
                f"Model '{model_name}' fitted successfully on {len(X_df)} observations"
            )
        except Exception as e:
            self.messenger.show_error("Fitting error", str(e))

    def _validate_configuration(self) -> bool:
        """Validate selected dependent and independent variables."""
        selected_x = self.independent_selector.get_selected_items()
        if not selected_x:
            self.messenger.show_error("Validation error", "Please select at least one independent variable")
            return False
        
        y_var = self.dependent_combo.currentText()
        if y_var in selected_x:
            self.messenger.show_error("Validation error", "Dependent variable cannot be in independent variables list")
            return False
        
        return True