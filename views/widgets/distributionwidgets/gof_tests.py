from typing import Callable
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from models.stat_distributions import BaseDistribution
from models import DataModel
from controllers import GOFController
from utils import EventBus, EventType, Event, AppContext
from views.widgets.distributionwidgets.gof_panels.base import BaseTestPanel
from views.widgets.utils import create_section_header, make_button
from views.widgets.utils.common_widgets import AlphaControlWidget


class GOFTestsWidget(QWidget):
    """A widget for evaluating Goodness-of-Fit (GOF) tests."""
    def __init__(self, context: AppContext,
                 gof_controller: GOFController,
                 test_panels: list[type[BaseTestPanel]],
                 multi_test_panels: list[type[BaseTestPanel]],
                 get_dist_func: Callable[[], BaseDistribution | None] | None = None) -> None:
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.get_dist_func = get_dist_func
        self.test_panels = [panel(gof_controller) for panel in test_panels]
        self.multi_test_panels = [panel(gof_controller) for panel in multi_test_panels]

        self._init_ui()
        self._subscribe_to_events()

    def _init_ui(self) -> None:
        """Initialize user interface and layout structure."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        controls_layout = QHBoxLayout()
        self.alpha_control = AlphaControlWidget()
        
        self.run_button = make_button(
            "Run Tests", 
            callback=lambda: self.evaluate_tests(multi=True),
            enabled=False,
            height=30
        )

        controls_layout.addWidget(self.alpha_control)
        controls_layout.addWidget(self.run_button)
        controls_layout.addStretch()

        layout.addLayout(controls_layout)

        # univariate
        layout.addLayout(create_section_header("Univariate tests"))
        for panel in self.test_panels:
            layout.addWidget(panel)

        # multivariate
        layout.addLayout(create_section_header("Multivariate tests"))
        for panel in self.multi_test_panels:
            layout.addWidget(panel)

        layout.addStretch()

    def _subscribe_to_events(self) -> None:
        """Subscribe widget to data state changes on EventBus."""
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_ready)
        self.event_bus.subscribe(EventType.DATA_TRANSFORMED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATA_REVERTED, self._on_data_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.COLUMN_CHANGED, self._on_data_changed)
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._on_data_ready)
        self.event_bus.subscribe(EventType.MISSING_VALUES_DETECTED, self._on_missings)

    def _on_data_ready(self, event: Event) -> None:
        """Enable Run button when data is available and clean."""
        self.run_button.setEnabled(True)

    def _on_data_changed(self, event: Event) -> None:
        """Clear results and re-enable Run button so user re-runs manually."""
        self.clear_panels()
        self.run_button.setEnabled(True)

    def _on_missings(self, event: Event) -> None:
        """Disable Run button and clear results when missing values are detected."""
        self.run_button.setEnabled(False)
        self.clear_panels()

    def evaluate_tests(self, multi: bool = True) -> None:
        """Run all GOF tests. Called by the Run button."""
        if self.get_dist_func is None:
            raise RuntimeError("No distribution access. Call `set_distribution_access` first.")
        dist = self.get_dist_func()
        model = self.context.data_model
        if model is None:
            return

        alpha = self.alpha_control.value()
        if dist is not None:
            self._evaluate_simple_tests(model, dist, alpha)
            if multi:
                self._evaluate_multi_tests(model, dist, alpha)

    def _evaluate_simple_tests(self, model: DataModel, dist: BaseDistribution, alpha: float) -> None:
        """Evaluate simple 1D tests for active series."""
        series = model.series.dropna()
        if series.empty:
            return
        for test in self.test_panels:
            test.evaluate(series, dist, alpha)

    def _evaluate_multi_tests(self, model: DataModel, dist: BaseDistribution, alpha: float) -> None:
        """Evaluate multivariate tests for active dataframe."""
        df = model.dataframe.dropna()
        if df.empty or df.shape[1] < 2:
            return
        for test in self.multi_test_panels:
            test.evaluate(df, dist, alpha)

    def clear_panels(self) -> None:
        """Clear test output in all registered test panels."""
        for test in [*self.test_panels, *self.multi_test_panels]:
            test.clear()

    def set_distribution_access(self, get_dist_func: Callable[[], BaseDistribution]) -> None:
        """Inject callback function to retrieve active distribution instance."""
        self.get_dist_func = get_dist_func