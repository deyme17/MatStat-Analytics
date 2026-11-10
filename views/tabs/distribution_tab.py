from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QScrollArea
)
from PyQt6.QtCore import Qt

from controllers import DistributionRegister
from models.stat_distributions import BaseDistribution
from views.widgets.distributionwidgets import (
    ParamEstimationWidget, GOFTestsWidget
)
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import make_group_box


class DistributionTab(QWidget):
    """
    Single tab that owns the distribution selection and hosts
    the parameter estimation and goodness-of-fit widgets.
    """
    def __init__(self,
                 dist_register: DistributionRegister,
                 param_estimation_widget: ParamEstimationWidget,
                 gof_tests_widget: GOFTestsWidget) -> None:
        """
        Args:
            dist_register: Register of available distributions.
            param_estimation_widget: ParamEstimationWidget
            gof_tests_widget: GOFTestWidget
        """
        super().__init__()
        self.dist_register = dist_register

        self.dist_combo = QComboBox()
        self.dist_combo.addItems(self.dist_register.distributions)

        self.param_widget = param_estimation_widget
        self.param_widget.set_distribution_access(self.get_distribution)
        self.gof_widget = gof_tests_widget
        self.gof_widget.set_distribution_access(self.get_distribution)

        self._init_ui()
        self.dist_combo.currentTextChanged.connect(self._on_distribution_changed)

    def _init_ui(self) -> None:
        """Initialize and layout all UI components."""
        container = QWidget()
        container.setStyleSheet(groupStyle + groupMargin)
        container_layout = QVBoxLayout(container)

        container_layout.addWidget(make_group_box(
            "Distribution",
            self._build_selector(),
        ))
        container_layout.addWidget(make_group_box(
            "Parameter Estimation",
            self.param_widget,
        ))
        container_layout.addWidget(make_group_box(
            "Goodness-of-Fit Tests",
            self.gof_widget,
        ))
        container_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)

    def _build_selector(self) -> QWidget:
        """Distribution combo with a short hint about what it affects."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Distribution:"))
        layout.addWidget(self.dist_combo)
        return widget

    def get_distribution(self) -> BaseDistribution | None:
        """Return a fresh instance of the currently selected distribution."""
        dist_class = self.dist_register.get_dist(self.dist_combo.currentText())
        return dist_class() if dist_class else None

    def _on_distribution_changed(self, _name: str) -> None:
        self.param_widget.clear_results()
        self.gof_widget.clear_panels()