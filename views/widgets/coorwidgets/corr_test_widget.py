from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, 
    QHBoxLayout, QLineEdit
)
from typing import Callable
from services.ui_services.messager import UIMessager
from utils import AppContext, EventBus, EventType, Event
from controllers import CorrelationController
from utils.ui_styles import groupMargin, groupStyle

HEADING_TITLE_SIZE = 10
DEFAULT_ALPHA_VAL_LABEL = "0.05"
MAX_ALPHA_INPUT_WIDTH = 100


class CorrelationTestWidget(QWidget):
    """Widget for generating and saving data from distributions."""
    def __init__(self, context: AppContext, corr_controller: CorrelationController):
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messanger: UIMessager = context.messanger
        self.controller: CorrelationController = corr_controller
        self.get_coeff_name = None
        self._init_ui()
        self._subscribe_to_events()
    
    def _init_ui(self) -> None:
        """Initialize correlation test UI components."""
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{'=' * HEADING_TITLE_SIZE} Test Correlation Significance {'=' * HEADING_TITLE_SIZE}"))
        self._init_alpha_controls(layout)
        self._init_column_selectors(layout)
        self._init_action_buttons(layout)
        self._init_result_section(layout)
        self.setLayout(layout)

    def _subscribe_to_events(self) -> None:
        """Subscribe to relevant events."""
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)

    def _init_alpha_controls(self, layout: QVBoxLayout) -> None:
        """Initialize significance level controls."""
        alpha_layout = QHBoxLayout()
        alpha_label = QLabel("Significance Level α:")
        self.alpha_input = QLineEdit()
        self.alpha_input.setText(DEFAULT_ALPHA_VAL_LABEL)
        self.alpha_input.setMaximumWidth(MAX_ALPHA_INPUT_WIDTH)
        alpha_layout.addWidget(alpha_label)
        alpha_layout.addWidget(self.alpha_input)
        alpha_layout.addStretch()
        layout.addLayout(alpha_layout)

    def _init_column_selectors(self, layout: QVBoxLayout) -> None:
        """Initialize column selectors for testing."""
        cols_layout = QHBoxLayout()
        self.x_col_combo = QComboBox()
        self.y_col_combo = QComboBox()
        cols_layout.addWidget(QLabel("X:"))
        cols_layout.addWidget(self.x_col_combo)
        cols_layout.addWidget(QLabel("Y:"))
        cols_layout.addWidget(self.y_col_combo)
        cols_layout.addStretch()
        layout.addLayout(cols_layout)

    def _init_action_buttons(self, layout: QVBoxLayout) -> None:
        """Add 'Run Test' button."""
        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("Run Test")
        self.run_btn.clicked.connect(self._run_test)
        btn_layout.addWidget(self.run_btn)
        layout.addLayout(btn_layout)

    def _init_result_section(self, layout: QVBoxLayout) -> None:
        """Initialize result section."""
        layout.addWidget(QLabel(f"{'=' * (HEADING_TITLE_SIZE + 4)} Testing Results {'=' * (HEADING_TITLE_SIZE + 4)}"))
        self.result_label = QLabel("No results yet.")
        self.result_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.result_label)

    def connect_coeff_combo(self, get_coeff_name: Callable[[None], str]) -> None:
        self.get_coeff_name = get_coeff_name

    def _on_data_changed(self, event: Event) -> None:
        self.x_col_combo.clear()
        self.y_col_combo.clear()

        data_model = self.context.data_model
        if data_model is None:
            return
        
        df = data_model.dataframe
        if df is not None and not df.empty:
            cols = list(df.columns)
            self.x_col_combo.addItems(cols)
            self.y_col_combo.addItems(cols)

    def _run_test(self) -> None:
        """Execute correlation test and show results."""
        if not self.get_coeff_name: ValueError("get_coeff_name not connected")

        data_model = self.context.data_model
        if data_model is None:
            return
        
        df = data_model.dataframe
        if df is None or df.empty:
            self.messanger.show_error("Error", "No data available.")
            return

        x_name = self.x_col_combo.currentText()
        y_name = self.y_col_combo.currentText()
        if not x_name or not y_name:
            self.messanger.show_error("Error", "Please select both X and Y columns.")
            return

        x, y = df[x_name], df[y_name]
        coeff_name = self.get_coeff_name()
        if not coeff_name:
            return

        try:
            # calculate coefficient
            r = self.controller.calculate(coeff_name, x, y)
            alpha = float(self.alpha_input.text())
            # test significance
            sig_result = self.controller.test_significance(coeff_name, x, y, alpha)
            # interpret result
            result_text =   f"""
                                Coefficient: {coeff_name}
                                r = {r:.4f}

                                {sig_result}
                            """
        
            self.result_label.setText(result_text.strip())
        except Exception as e:
            self.messanger.show_error("Error", f"{e}")