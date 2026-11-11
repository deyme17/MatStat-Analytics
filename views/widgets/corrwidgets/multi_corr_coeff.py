from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
)
from services.ui_services.messager import UIMessager
from controllers import CorrelationController
from utils import AppContext, EventBus, EventType, Event
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import create_section_header, make_button
from views.widgets.utils.common_widgets import FeatureSelectorWidget, AlphaControlWidget


class MultiCorrWidget(QWidget):
    """
    Widget for multiple correlation coefficient (R).
    Allows selecting one dependent variable Y and multiple predictors.
    """
    def __init__(self, context: AppContext, corr_controller: CorrelationController):
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messanger: UIMessager = context.messanger
        self.controller: CorrelationController = corr_controller
        
        self._init_ui()
        self._subscribe_to_events()

    def _init_ui(self) -> None:
        """Initialize multiple correlation test UI components."""
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout()
        layout.addLayout(create_section_header("Multiple Correlation"))

        self.alpha_control = AlphaControlWidget()
        layout.addWidget(self.alpha_control)

        # y selector
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Dependent variable Y:"))
        self.y_combo = QComboBox()
        y_layout.addWidget(self.y_combo)
        y_layout.addStretch()
        layout.addLayout(y_layout)

        # X selector
        self.predictors_selector = FeatureSelectorWidget(
            title="Predictors (X)",
            label_prefix="predictors",
            height=120
        )
        layout.addWidget(self.predictors_selector)

        # run btn
        btn_layout = QHBoxLayout()
        self.run_btn = make_button("Run Multiple Correlation", callback=self._run_test, height=32)
        btn_layout.addWidget(self.run_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # result
        layout.addLayout(create_section_header("Testing Results"))
        self.result_label = QLabel("No results yet.")
        self.result_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.result_label)

        layout.addStretch()
        self.setLayout(layout)

    def _subscribe_to_events(self) -> None:
        """Subscribe to data update events."""
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)

    def _on_data_changed(self, event: Event) -> None:
        """Repopulate dependent variable combo and predictors list."""
        self.y_combo.clear()
        
        data_model = self.context.data_model
        if data_model is None:
            return

        df = data_model.dataframe
        if df is not None and not df.empty:
            cols = list(df.columns)
            self.y_combo.addItems(cols)
            self.predictors_selector.populate(cols, select_all=False)

    def _run_test(self) -> None:
        """Perform multiple correlation analysis and test significance."""
        data_model = self.context.data_model
        if data_model is None or data_model.dataframe is None or data_model.dataframe.empty:
            self.messanger.show_error("Error", "No data available.")
            return

        df = data_model.dataframe
        y_name = self.y_combo.currentText()
        predictor_names = self.predictors_selector.get_selected_items()

        if not y_name:
            self.messanger.show_error("Error", "Please select dependent variable Y.")
            return
        if not predictor_names:
            self.messanger.show_error("Error", "Please select at least one predictor.")
            return
        if y_name in predictor_names:
            self.messanger.show_error("Error", "Y cannot also be selected as a predictor.")
            return

        try:
            alpha = self.alpha_control.value()
            y = df[y_name]
            predictors = [df[p] for p in predictor_names]

            result = self.controller.test_multiple_correlation_significance(y, predictors, alpha)
            self.result_label.setText(str(result).strip())
        except Exception as e:
            self.messanger.show_error("Error", f"{e}")