from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from services import UIMessager, DataVersionManager
from utils import AppContext, EventBus, EventType, Event
from controllers import HomogenController
from views.widgets.homogenwidgets.panels.homogen_panel import BaseHomoTestPanel
from views.widgets.homogenwidgets import HomoDataSelectorWidget, HomoTestSectionGroup
from views.widgets.utils.common_widgets import AlphaControlWidget
from utils.ui_styles import groupMargin, groupStyle


class HomogenTab(QWidget):
    """Tab widget for homogeneity tests."""
    def __init__(self, context: AppContext, homogen_controller: HomogenController,
                                            homogen_2samples_panels: list[BaseHomoTestPanel],
                                            homogen_Nsamples_panels: list[BaseHomoTestPanel],
                                            hamogen_1sample_panels: list[BaseHomoTestPanel]) -> None:
        """
        Args:
            homogen_controller (HomogenController): Controller to perform Homogeneity tests.
            context: Shared application context (version_manager, event_bus, messager)
            homogen_2samples_panels (list): List of Homogeneity test panel classes for two samples test.
            homogen_Nsamples_panels (list): List of Homogeneity test panel classes for N samples test.
            hamogen_1sample_panels (list): List of Homogeneity test panel classes for 1 samples test.
        """
        super().__init__()
        self.homogen_controller: HomogenController = homogen_controller
        self.version_manager: DataVersionManager = context.version_manager
        self.messanger: UIMessager = context.messanger
        self.event_bus: EventBus = context.event_bus
        self.selected_models: list[str] = []

        self.two_samples_panels = [pnl(homogen_controller) for pnl in homogen_2samples_panels]
        self.n_samples_panels = [pnl(homogen_controller) for pnl in homogen_Nsamples_panels]
        self.hamogen_1sample_panels = [pnl(homogen_controller) for pnl in hamogen_1sample_panels]

        self._setup_ui()
        self._connect_signals()
        self._refresh_data_list()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        """Subscribe to application events."""
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_loaded)

    def _on_data_loaded(self, event: Event) -> None:
        """Handle data load event."""
        self._refresh_data_list()

    def _setup_ui(self) -> None:
        """Setup the user interface layout."""
        self.setStyleSheet(groupStyle + groupMargin)
        main_layout = QVBoxLayout()

        self.alpha_control = AlphaControlWidget()
        main_layout.addWidget(self.alpha_control)

        self.selector_widget = HomoDataSelectorWidget()
        main_layout.addWidget(self.selector_widget)

        main_layout.addWidget(HomoTestSectionGroup(
            "Homogeneity tests for two samples", self.two_samples_panels, self._run_selected_test
        ))
        main_layout.addWidget(HomoTestSectionGroup(
            "Homogeneity tests for multiple samples", self.n_samples_panels, self._run_selected_test
        ))
        main_layout.addWidget(HomoTestSectionGroup(
            "Tests for one sample", self.hamogen_1sample_panels, self._run_selected_test
        ))

        main_layout.addStretch()

        container = QWidget()
        container.setLayout(main_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(scroll)

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        self.selector_widget.list_widget.itemSelectionChanged.connect(self._update_selected_models)

    def _refresh_data_list(self) -> None:
        """Refresh the data models list."""
        valid_names = [
            name for name, model in (self.version_manager.datasets or {}).items()
            if model.series is not None and not model.series.empty
        ]
        self.selector_widget.populate(valid_names, select_all=False)

    def _update_selected_models(self) -> None:
        """Update selected models list and label."""
        self.selected_models = self.selector_widget.get_selected_items()
        self.selector_widget.update_count_label()

    def _run_selected_test(self, group: HomoTestSectionGroup) -> None:
        """Run selected panel in the group."""
        if not self.selected_models:
            self.messanger.show_error("Test running error", "Please select at least one dataset")
            return

        datasets = self.version_manager.datasets
        panel = group.get_selected_panel()
        if not panel:
            return

        for pnl in group.panels:
            pnl.hide()

        try:
            support_multivariate = getattr(panel, "support_multivariate", False)
            if support_multivariate:
                samples = [datasets[name].dataframe for name in self.selected_models]
            else:
                samples = [datasets[name].series for name in self.selected_models]

            panel.evaluate(
                samples=samples,
                alpha=self.alpha_control.value(),
                is_independent=self.selector_widget.is_independent()
            )
            panel.show()
        except Exception as e:
            panel.clear()
            self.messanger.show_error("Test running error", str(e))