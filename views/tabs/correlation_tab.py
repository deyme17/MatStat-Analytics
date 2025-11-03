from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from utils import AppContext, EventBus, EventType
from services import UIMessager
from controllers import CorrelationController


class CorrelationTab(QWidget):
    """
    Tab for selecting correlation coefficient.
    Emits event on selection change to notify dependent components.
    """
    def __init__(self, context: AppContext, corr_controller: CorrelationController, corr_test_widget=None):
        """
        Args:
            context: AppContext with data_model and messenger
            corr_controller: CorrelationController instance
            corr_test_widget: Optional widget for correlation test parameters
        """
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messenger: UIMessager = context.messanger
        self.controller: CorrelationController = corr_controller
        self.test_widget = corr_test_widget

        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize and layout all UI components."""
        layout = QVBoxLayout()

        self.corr_combo = QComboBox()
        coeff_names = list(self.controller._tests.keys())
        if not coeff_names:
            coeff_names = ["-"]

        self.corr_combo.addItems(coeff_names)
        self._on_corr_changed()
        self.corr_combo.currentIndexChanged.connect(self._on_corr_changed)

        layout.addWidget(QLabel("Select Correlation Coefficient:"))
        layout.addWidget(self.corr_combo)

        if self.test_widget:
            layout.addWidget(self.test_widget)

        layout.addStretch()
        self.setLayout(layout)

    def _on_corr_changed(self) -> None:
        """Emit event when correlation coefficient selection changes."""
        selected = self.corr_combo.currentText()
        self.event_bus.emit_type(EventType.CORR_COEFF_CHANGED, selected)