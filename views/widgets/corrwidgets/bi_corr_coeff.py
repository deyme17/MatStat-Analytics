from typing import Callable
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
)
from services.ui_services.messager import UIMessager
from controllers import CorrelationController
from utils import AppContext, EventBus, EventType, Event
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import create_section_header, make_button
from views.widgets.utils.common_widgets import AlphaControlWidget


class BivariateCorrWidget(QWidget):
    """Widget for testing bivariate correlation significance."""
    def __init__(self, context: AppContext, corr_controller: CorrelationController):
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messanger: UIMessager = context.messanger
        self.controller: CorrelationController = corr_controller
        self.get_coeff_name: Callable[[], str] | None = None
        
        self._init_ui()
        self._subscribe_to_events()
    
    def _init_ui(self) -> None:
        """Initialize correlation test UI components."""
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout()
        
        layout.addLayout(create_section_header("Test Correlation Significance"))
        
        self.alpha_control = AlphaControlWidget()
        layout.addWidget(self.alpha_control)
        
        self._init_column_selectors(layout)
        self._init_action_buttons(layout)
        self._init_result_section(layout)
        
        layout.addStretch()
        self.setLayout(layout)

    def _subscribe_to_events(self) -> None:
        """Subscribe to data model update events."""
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)

    def _init_column_selectors(self, layout: QVBoxLayout) -> None:
        """Initialize X and Y column selectors for testing."""
        xy_layout = QHBoxLayout()
        self.x_col_combo = QComboBox()
        self.y_col_combo = QComboBox()
        
        xy_layout.addWidget(QLabel("X:"))
        xy_layout.addWidget(self.x_col_combo)
        xy_layout.addWidget(QLabel("Y:"))
        xy_layout.addWidget(self.y_col_combo)
        xy_layout.addStretch()
        
        layout.addLayout(xy_layout)

    def _init_action_buttons(self, layout: QVBoxLayout) -> None:
        """Add action button for running the correlation test."""
        btn_layout = QHBoxLayout()
        self.run_btn = make_button("Run Test", callback=self._run_test, height=32)
        btn_layout.addWidget(self.run_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def _init_result_section(self, layout: QVBoxLayout) -> None:
        """Initialize result section for output display."""
        layout.addLayout(create_section_header("Testing Results"))
        self.result_label = QLabel("No results yet.")
        self.result_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.result_label)

    def connect_coeff_combo(self, get_coeff_name: Callable[[], str]) -> None:
        """Attach external callback returning selected correlation coefficient name."""
        self.get_coeff_name = get_coeff_name

    def _on_data_changed(self, event: Event) -> None:
        """Update available column choices when dataset changes."""
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
        """Execute bivariate correlation significance test."""
        if not self.get_coeff_name:
            raise ValueError("get_coeff_name callback is not connected")

        data_model = self.context.data_model
        if data_model is None or data_model.dataframe is None or data_model.dataframe.empty:
            self.messanger.show_error("Error", "No data available.")
            return

        df = data_model.dataframe
        x_name = self.x_col_combo.currentText()
        y_name = self.y_col_combo.currentText()
        
        if not x_name or not y_name:
            self.messanger.show_error("Error", "Please select both X and Y columns.")
            return

        coeff_name = self.get_coeff_name()
        if not coeff_name:
            return

        try:
            x, y = df[x_name], df[y_name]
            alpha = self.alpha_control.value()
            
            sig_result = self.controller.test_significance(coeff_name, x, y, alpha)
            self.result_label.setText(str(sig_result).strip())
        except Exception as e:
            self.messanger.show_error("Error", f"{e}")