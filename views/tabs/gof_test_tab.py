from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDoubleSpinBox, QHBoxLayout, QPushButton
from models.stat_distributions import StatisticalDistribution
from models import DataModel
from views.widgets.gofwidgets.gof_test_panel import BaseTestPanel
from typing import Callable
from controllers import GOFController
from utils import EventBus, EventType, Event, AppContext


ALPHA_MIN, ALPHA_MAX = 0.01, 0.99
ALPHA_STEP = 0.01
ALPHA_PRECISION = 2
DEFAULT_ALPHA = 0.05
HEADING_TITLE_SIZE = 16



class GOFTestTab(QWidget):
    """
    A tab widget for evaluating Goodness-of-Fit (GOF) tests.
    """
    def __init__(self, context: AppContext,
                 get_dist_func: Callable[[None], StatisticalDistribution],
                 gof_controller: GOFController,
                 test_panels: list[BaseTestPanel],
                 multi_test_panels: list[BaseTestPanel]) -> None:
        """
        Args:
            context: Shared application context (data_model, event_bus, messager).
            get_dist_func: Function for access to selected distribution.
            gof_controller: Controller for performing goodness-of-fit tests.
            test_panels: List of goodness-of-fit test pabels (univariate).
            multi_test_panels: List of goodness-of-fit test pabels (multivariate).
        """
        super().__init__()
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.get_dist_func = get_dist_func
        self.test_panels = [panel(gof_controller) for panel in test_panels]
        self.multi_test_panels = [panel(gof_controller) for panel in multi_test_panels]

        self.alpha_spinbox = QDoubleSpinBox()
        self.alpha_spinbox.setRange(ALPHA_MIN, ALPHA_MAX)
        self.alpha_spinbox.setSingleStep(ALPHA_STEP)
        self.alpha_spinbox.setDecimals(ALPHA_PRECISION)
        self.alpha_spinbox.setValue(DEFAULT_ALPHA)

        self.run_button = QPushButton("Run Tests")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.evaluate_tests)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Significance level α:"))
        controls_layout.addWidget(self.alpha_spinbox)
        controls_layout.addWidget(self.run_button)
        controls_layout.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(controls_layout)

        layout.addWidget(QLabel(f"{HEADING_TITLE_SIZE * '='} Simple tests {HEADING_TITLE_SIZE * '='}"))
        for panel in self.test_panels:
            layout.addWidget(panel)

        layout.addWidget(QLabel(f"{HEADING_TITLE_SIZE * '='} Multivariate tests {HEADING_TITLE_SIZE * '='}"))
        for panel in self.multi_test_panels:
            layout.addWidget(panel)

        layout.addStretch()
        self.setLayout(layout)

        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
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
        dist  = self.get_dist_func()
        model = self.context.data_model
        if model is None:
            return

        alpha = self.alpha_spinbox.value()

        if dist is not None:
            self._evaluate_simple_tests(model, dist, alpha)
        if multi:
            self._evaluate_multi_tests(model, dist, alpha)

    def _evaluate_simple_tests(self, model: DataModel, dist: StatisticalDistribution, alpha: float) -> None:
        series = model.series.dropna()
        if series.empty:
            return
        for test in self.test_panels:
            test.evaluate(series, dist, alpha)

    def _evaluate_multi_tests(self, model: DataModel, dist: StatisticalDistribution, alpha: float) -> None:
        df = model.dataframe.dropna()
        if df.empty or df.shape[1] < 2:
            return
        for test in self.multi_test_panels:
            test.evaluate(df, dist, alpha)

    def clear_panels(self) -> None:
        for test in [*self.test_panels, *self.multi_test_panels]:
            test.clear()