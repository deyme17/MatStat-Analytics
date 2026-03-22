from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QHBoxLayout, QLineEdit, QListWidget,
    QAbstractItemView
)
from services.ui_services.messager import UIMessager
from utils import AppContext, EventBus, EventType, Event
from controllers import CorrelationController
from utils.ui_styles import groupMargin, groupStyle

HEADING_TITLE_SIZE = 10
DEFAULT_ALPHA_VAL_LABEL = "0.05"
MAX_ALPHA_INPUT_WIDTH = 100


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
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{'=' * HEADING_TITLE_SIZE} Multiple Correlation {'=' * HEADING_TITLE_SIZE}"))

        # alpha
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Significance Level α:"))
        self.alpha_input = QLineEdit(DEFAULT_ALPHA_VAL_LABEL)
        self.alpha_input.setMaximumWidth(MAX_ALPHA_INPUT_WIDTH)
        alpha_layout.addWidget(self.alpha_input)
        alpha_layout.addStretch()
        layout.addLayout(alpha_layout)

        # dependent variable Y
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Dependent variable Y:"))
        self.y_combo = QComboBox()
        y_layout.addWidget(self.y_combo)
        y_layout.addStretch()
        layout.addLayout(y_layout)

        # predictors (multi-select list)
        layout.addWidget(QLabel("Predictors (Ctrl+Click for multiple):"))
        self.predictors_list = QListWidget()
        self.predictors_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.predictors_list.setMaximumHeight(100)
        layout.addWidget(self.predictors_list)

        # run button
        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("Run Multiple Correlation")
        self.run_btn.clicked.connect(self._run_test)
        btn_layout.addWidget(self.run_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # result
        layout.addWidget(QLabel(f"{'=' * (HEADING_TITLE_SIZE + 4)} Testing Results {'=' * (HEADING_TITLE_SIZE + 4)}"))
        self.result_label = QLabel("No results yet.")
        self.result_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.result_label)

        layout.addStretch()
        self.setLayout(layout)

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)

    def _on_data_changed(self, event: Event) -> None:
        self.y_combo.clear()
        self.predictors_list.clear()

        data_model = self.context.data_model
        if data_model is None:
            return

        df = data_model.dataframe
        if df is not None and not df.empty:
            cols = list(df.columns)
            self.y_combo.addItems(cols)
            self.predictors_list.addItems(cols)

    def _run_test(self) -> None:
        data_model = self.context.data_model
        if data_model is None:
            return

        df = data_model.dataframe
        if df is None or df.empty:
            self.messanger.show_error("Error", "No data available.")
            return

        y_name = self.y_combo.currentText()
        predictor_names = [item.text() for item in self.predictors_list.selectedItems()]

        if not y_name:
            self.messanger.show_error("Error", "Please select dependent variable Y.")
            return
        if not predictor_names:
            self.messanger.show_error("Error", "Please select at least one predictor.")
            return
        if y_name in predictor_names:
            self.messanger.show_error("Error", "Y cannot also be a predictor.")
            return

        try:
            alpha = float(self.alpha_input.text())
            y = df[y_name]
            predictors = [df[p] for p in predictor_names]

            result = self.controller.test_multiple_correlation_significance(y, predictors, alpha)
            self.result_label.setText(str(result).strip())
        except Exception as e:
            self.messanger.show_error("Error", f"{e}")