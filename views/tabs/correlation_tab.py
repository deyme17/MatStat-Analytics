from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTabWidget
from utils import AppContext, EventBus, EventType
from services import UIMessager
from views.widgets.coorwidgets import CorrelationTestWidget
from views.widgets.coorwidgets.part_corr_coeffs_widget import PartialCorrWidget
from views.widgets.coorwidgets.multi_corr_coeff_widget import MultiCorrWidget
from controllers import CorrelationController
from utils.ui_styles import groupMargin, groupStyle


class CorrelationTab(QWidget):
    """
    Tab for correlation analysis.
    Contains three sub-tabs:
      - Bivariate: classic pairwise correlation with significance test
      - Partial: partial correlation controlling for one or more variables
      - Multiple: multiple correlation R with F-test
    """
    def __init__(
        self,
        context: AppContext,
        corr_controller: CorrelationController,
        corr_test_widget: type[CorrelationTestWidget],
        partial_corr_widget: type[PartialCorrWidget],
        multi_corr_widget: type[MultiCorrWidget]
    ):
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.messenger: UIMessager = context.messanger
        self.controller: CorrelationController = corr_controller

        self.test_widget = corr_test_widget(context, corr_controller)
        self.partial_widget = partial_corr_widget(context, corr_controller)
        self.multiple_widget = multi_corr_widget(context, corr_controller)

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

        self.test_widget.connect_coeff_combo(lambda: self.corr_combo.currentText())
        self._on_corr_changed()

        # sub-tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.test_widget,    "Bivariate")
        self.tabs.addTab(self.partial_widget, "Partial")
        self.tabs.addTab(self.multiple_widget,"Multiple")
        layout.addWidget(self.tabs)

        layout.addStretch()
        self.setLayout(layout)

    def _on_corr_changed(self) -> None:
        """Emit event when bivariate coefficient selection changes."""
        selected = self.corr_combo.currentText()
        self.event_bus.emit_type(EventType.CORR_COEFF_CHANGED, selected)