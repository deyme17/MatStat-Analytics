from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
)
from services.ui_services.messager import UIMessager
from controllers import CorrelationController
from utils import AppContext, EventBus, EventType, Event
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import create_section_header, make_button
from views.widgets.utils.common_widgets import FeatureSelectorWidget, AlphaControlWidget


class PartialCorrWidget(QWidget):
    """
    Widget for partial correlation coefficient.
    Allows selecting X, Y, and one or more control variables.
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
        """Initialize partial correlation test UI components."""
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout()
        layout.addLayout(create_section_header("Partial Correlation"))

        self.alpha_control = AlphaControlWidget()
        layout.addWidget(self.alpha_control)

        # (x, y) selectors
        xy_layout = QHBoxLayout()
        self.x_combo = QComboBox()
        self.y_combo = QComboBox()
        
        xy_layout.addWidget(QLabel("X:"))
        xy_layout.addWidget(self.x_combo)
        xy_layout.addWidget(QLabel("Y:"))
        xy_layout.addWidget(self.y_combo)
        xy_layout.addStretch()
        layout.addLayout(xy_layout)

        # control var selector
        self.controls_selector = FeatureSelectorWidget(
            title="Control Variables (Z)",
            label_prefix="variables",
            height=120
        )
        layout.addWidget(self.controls_selector)

        # run btn
        btn_layout = QHBoxLayout()
        self.run_btn = make_button("Run Partial Correlation", callback=self._run_test, height=32)
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
        """Repopulate column selectors and control variables list."""
        self.x_combo.clear()
        self.y_combo.clear()

        data_model = self.context.data_model
        if data_model is None:
            return

        df = data_model.dataframe
        if df is not None and not df.empty:
            cols = list(df.columns)
            self.x_combo.addItems(cols)
            self.y_combo.addItems(cols)
            self.controls_selector.populate(cols, select_all=False)

    def _run_test(self) -> None:
        """Perform partial correlation test and display results."""
        data_model = self.context.data_model
        if data_model is None or data_model.dataframe is None or data_model.dataframe.empty:
            self.messanger.show_error("Error", "No data available.")
            return

        df = data_model.dataframe
        x_name = self.x_combo.currentText()
        y_name = self.y_combo.currentText()
        control_names = self.controls_selector.get_selected_items()

        if not x_name or not y_name:
            self.messanger.show_error("Error", "Please select both X and Y columns.")
            return
        if not control_names:
            self.messanger.show_error("Error", "Please select at least one control variable.")
            return
        if x_name == y_name:
            self.messanger.show_error("Error", "X and Y must be different columns.")
            return
        if x_name in control_names or y_name in control_names:
            self.messanger.show_error("Error", "X and Y cannot be included in control variables.")
            return

        try:
            alpha = self.alpha_control.value()
            x = df[x_name]
            y = df[y_name]
            controls = [df[c] for c in control_names]

            result = self.controller.test_partial_correlation_significance(x, y, controls, alpha)
            self.result_label.setText(str(result).strip())
        except Exception as e:
            self.messanger.show_error("Error", f"{e}")