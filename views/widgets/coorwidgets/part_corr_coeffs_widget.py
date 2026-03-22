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
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{'=' * HEADING_TITLE_SIZE} Partial Correlation {'=' * HEADING_TITLE_SIZE}"))

        # alpha
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Significance Level α:"))
        self.alpha_input = QLineEdit(DEFAULT_ALPHA_VAL_LABEL)
        self.alpha_input.setMaximumWidth(MAX_ALPHA_INPUT_WIDTH)
        alpha_layout.addWidget(self.alpha_input)
        alpha_layout.addStretch()
        layout.addLayout(alpha_layout)

        # X and Y selectors
        xy_layout = QHBoxLayout()
        self.x_combo = QComboBox()
        self.y_combo = QComboBox()
        xy_layout.addWidget(QLabel("X:"))
        xy_layout.addWidget(self.x_combo)
        xy_layout.addWidget(QLabel("Y:"))
        xy_layout.addWidget(self.y_combo)
        xy_layout.addStretch()
        layout.addLayout(xy_layout)

        # control variables (multi-select list)
        layout.addWidget(QLabel("Control variables (Ctrl+Click for multiple):"))
        self.controls_list = QListWidget()
        self.controls_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.controls_list.setMaximumHeight(100)
        layout.addWidget(self.controls_list)

        # run button
        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("Run Partial Correlation")
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
        self.x_combo.clear()
        self.y_combo.clear()
        self.controls_list.clear()

        data_model = self.context.data_model
        if data_model is None:
            return

        df = data_model.dataframe
        if df is not None and not df.empty:
            cols = list(df.columns)
            self.x_combo.addItems(cols)
            self.y_combo.addItems(cols)
            self.controls_list.addItems(cols)

    def _run_test(self) -> None:
        data_model = self.context.data_model
        if data_model is None:
            return

        df = data_model.dataframe
        if df is None or df.empty:
            self.messanger.show_error("Error", "No data available.")
            return

        x_name = self.x_combo.currentText()
        y_name = self.y_combo.currentText()
        control_names = [item.text() for item in self.controls_list.selectedItems()]

        if not x_name or not y_name:
            self.messanger.show_error("Error", "Please select both X and Y columns.")
            return
        if not control_names:
            self.messanger.show_error("Error", "Please select at least one control variable.")
            return
        if x_name == y_name:
            self.messanger.show_error("Error", "X and Y must be different columns.")
            return

        try:
            alpha = float(self.alpha_input.text())
            x = df[x_name]
            y = df[y_name]
            controls = [df[c] for c in control_names]

            result = self.controller.test_partial_correlation_significance(x, y, controls, alpha)
            self.result_label.setText(str(result).strip())
        except Exception as e:
            self.messanger.show_error("Error", f"{e}")