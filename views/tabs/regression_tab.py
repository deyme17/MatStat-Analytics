from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt

from views.widgets.regressionwidgets import RegrSummaryWidget, RegrPredictionWidget
from views.widgets.regressionwidgets import RegrModelSelectorWidget, RegrDependentVarSelectorWidget
from views.widgets.utils.common_widgets import FeatureSelectorWidget
from views.widgets.utils.common_widgets import AlphaControlWidget
from utils import AppContext, EventBus, EventType, Event
from services import UIMessager
from controllers import RegressionController
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import make_button

LIST_WIDGET_HEIGHT = 100
LIST_WIDGET_WIDTH = 330
MAX_GROUP_HEIGHT = 150


class RegressionTab(QWidget):
    """Tab for conducting regression analysis."""
    def __init__(self, context: AppContext, regr_controller: RegressionController):
        """
        Args:
            context: AppContext with data_model, event_bus and messenger
            regr_controller: controller for performing regression steps (fitting -> evaluating -> prediction)
        """
        super().__init__()
        self.context: AppContext = context
        self.messenger: UIMessager = context.messanger
        self.event_bus: EventBus = context.event_bus
        self.controller: RegressionController = regr_controller

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
        container_layout = QVBoxLayout(container)

        self.model_selector = RegrModelSelectorWidget(self.controller.regression_models)
        container_layout.addWidget(self.model_selector)

        self.independent_selector = FeatureSelectorWidget(
            title="Independent Variables (X)", 
            label_prefix="variables", 
            height=LIST_WIDGET_HEIGHT, 
            width=LIST_WIDGET_WIDTH
        )
        self.independent_selector.setMaximumHeight(MAX_GROUP_HEIGHT)
        container_layout.addWidget(self.independent_selector)

        self.dependent_selector = RegrDependentVarSelectorWidget()
        container_layout.addWidget(self.dependent_selector)

        self.fit_btn = make_button("Fit the model", callback=self._fit_model)
        container_layout.addWidget(self.fit_btn)

        self.alpha_control = AlphaControlWidget()
        self.alpha_control.alpha_changed.connect(self._on_alpha_changed)
        container_layout.addWidget(self.alpha_control)

        self.summary_widget = RegrSummaryWidget(self.context, self.controller)
        container_layout.addWidget(self.summary_widget)
        self.prediction_widget = RegrPredictionWidget(self.context, self.controller)
        container_layout.addWidget(self.prediction_widget)
        container_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        self.independent_selector.list_widget.itemSelectionChanged.connect(
            self.independent_selector.update_count_label
        )

    def _on_alpha_changed(self, alpha: float) -> None:
        """Handle alpha control value change."""
        self.summary_widget.create_summary(alpha)
        self.prediction_widget.set_alpha_value(alpha)

    def _refresh_data(self) -> None:
        """Refresh available datasets and feature options."""
        self.independent_selector.list_widget.clear()

        data_model = self.context.data_model
        if data_model is None or data_model.dataframe.empty: 
            return
        df = data_model.dataframe

        columns = sorted(list(set(df.columns)))
        self.independent_selector.populate(columns, select_all=False)
        self.dependent_selector.populate(columns)

    def _fit_model(self) -> None:
        """Fit a selected regression model."""
        if not self._validate_configuration():
            return
        self.summary_widget.clear()
        self.prediction_widget.clear()

        try:
            model_name = self.model_selector.get_selected_model()
            x_vars = self.independent_selector.get_selected_items()
            y_var = self.dependent_selector.get_selected_variable()

            data_model = self.context.data_model
            if data_model is None or data_model.dataframe.empty: 
                return
            df = data_model.dataframe

            missing_cols = [col for col in x_vars + [y_var] if col not in df.columns]
            if missing_cols:
                self.messenger.show_error("Fitting error", f"Missing columns: {', '.join(missing_cols)}")
                return

            X_df = df[x_vars]
            y_series = df[y_var]

            self.controller.fit(model_name, X_df, y_series)

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

        y_var = self.dependent_selector.get_selected_variable()
        if y_var in selected_x:
            self.messenger.show_error("Validation error", "Dependent variable cannot be in independent variables list")
            return False

        return True