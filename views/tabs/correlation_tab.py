from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTabWidget
from utils import AppContext, EventBus, EventType
from services import UIMessager
from views.widgets.corrwidgets import BivariateCorrWidget
from views.widgets.corrwidgets.part_corr_coeff import PartialCorrWidget
from views.widgets.corrwidgets.multi_corr_coeff import MultiCorrWidget
from controllers import CorrelationController
from utils.ui_styles import groupMargin, groupStyle


class CorrelationTab(QWidget):
    """
    Tab for correlation analysis. Contains three sub-tabs:
      - Bivariate: classic pairwise correlation with significance test
      - Partial: partial correlation controlling for one or more variables
      - Multiple: multiple correlation R with F-test
    """
    def __init__(self, context: AppContext, corr_controller: CorrelationController):
        """
        Args:
            context: Shared application context (data_model, event_bus, messager).
            corr_controller: Controller for performing correlation calculations.
        """
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messenger: UIMessager = context.messanger
        self.controller: CorrelationController = corr_controller

        self._init_ui()

    def _init_ui(self) -> None:
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout()

        # coefficient selector
        layout.addWidget(QLabel("Select Bivariate Correlation Coefficient:"))
        self.corr_combo = QComboBox()
        coeff_names = list(self.controller.corr_coeffs) or ["-"]
        self.corr_combo.addItems(coeff_names)
        self.corr_combo.currentIndexChanged.connect(self._on_corr_changed)
        layout.addWidget(self.corr_combo)

        self.bivariate_widget = BivariateCorrWidget(self.context, self.controller)
        self.bivariate_widget.connect_coeff_combo(lambda: self.corr_combo.currentText())
        self._on_corr_changed()

        # sub-tabs
        self.partial_widget = PartialCorrWidget(self.context, self.controller)
        self.multiple_widget = MultiCorrWidget(self.context, self.controller)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.bivariate_widget, "Bivariate")
        self.tabs.addTab(self.partial_widget, "Partial")
        self.tabs.addTab(self.multiple_widget,"Multiple")
        layout.addWidget(self.tabs)

        layout.addStretch()
        self.setLayout(layout)

    def _on_corr_changed(self) -> None:
        """Emit event when bivariate coefficient selection changes."""
        selected = self.corr_combo.currentText()
        self.event_bus.emit_type(EventType.CORR_COEFF_CHANGED, selected)