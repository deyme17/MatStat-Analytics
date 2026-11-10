from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QGroupBox, QComboBox, QScrollArea, QCheckBox
)
from services import UIMessager, DataVersionManager
from utils import AppContext, EventBus, EventType, Event
from controllers import HomogenController
from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel
from views.widgets.utils.common_widgets import FeatureSelectorWidget
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import make_alpha_spinbox, make_button

ALPHA_MIN, ALPHA_MAX = 0.01, 0.99
ALPHA_STEP = 0.01
ALPHA_PRECISION = 2
DEFAULT_ALPHA = 0.05

MAX_GROUP_HEIGHT = 159
LIST_WIDGET_HEIGHT = 150
LIST_WIDGET_WIDTH = 320


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
        self.selected_models = []

        # panels
        self.two_samples_panels = [pnl(homogen_controller) for pnl in homogen_2samples_panels]
        self.n_samples_panels = [pnl(homogen_controller) for pnl in homogen_Nsamples_panels]
        self.hamogen_1sample_panels = [pnl(homogen_controller) for pnl in hamogen_1sample_panels]

        self._setup_ui()
        self._connect_signals()
        self._refresh_data_list()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.DATA_LOADED, self._on_data_loaded)

    def _on_data_loaded(self, event: Event) -> None:
        self._refresh_data_list()

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        self.setStyleSheet(groupStyle + groupMargin)
        main_layout = QVBoxLayout()
        main_layout.addLayout(self._create_alpha_spinbox())
        main_layout.addWidget(self._create_data_selection_section())

        # test sections
        main_layout.addWidget(self._create_test_section("Homogeneity tests for two samples", self.two_samples_panels))
        main_layout.addWidget(self._create_test_section("Homogeneity tests for multiple samples", self.n_samples_panels))
        main_layout.addWidget(self._create_test_section("Tests for one sample", self.hamogen_1sample_panels))

        main_layout.addStretch()

        container = QWidget()
        container.setLayout(main_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scroll)
        self.setLayout(outer_layout)

    def _create_alpha_spinbox(self) -> QHBoxLayout:
        """Create alpha parameter selection section."""
        layout = QHBoxLayout()
        self.alpha_spinbox = make_alpha_spinbox(
            ALPHA_MIN, ALPHA_MAX, ALPHA_STEP, ALPHA_PRECISION, DEFAULT_ALPHA
        )
        layout.addWidget(QLabel("Significance level α:"))
        layout.addWidget(self.alpha_spinbox)
        layout.addStretch()
        return layout

    def _create_data_selection_section(self) -> QGroupBox:
        """Create data selection section."""
        self.selector_widget = FeatureSelectorWidget(
            title="Select datasets for testing",
            label_prefix="datasets",
            height=LIST_WIDGET_HEIGHT,
            width=LIST_WIDGET_WIDTH
        )
        self.list_widget = self.selector_widget.list_widget
        self.select_all_btn = self.selector_widget.select_all_btn
        self.clear_selection_btn = self.selector_widget.clear_sel_btn
        self.selected_count_label = self.selector_widget.count_label

        self.independence_checkbox = QCheckBox("Samples are independent")
        self.independence_checkbox.setChecked(False)

        layout = self.selector_widget.layout()
        layout.addWidget(self.independence_checkbox)

        self.selector_widget.setMaximumHeight(MAX_GROUP_HEIGHT)
        return self.selector_widget

    def _create_test_section(self, title: str, panels: list[BaseHomoTestPanel]) -> QGroupBox:
        """Create a test section with panels, run button, and clear button."""
        group = QGroupBox(title)
        layout = QVBoxLayout()

        combo = QComboBox()
        for panel in panels:
            combo.addItem(panel.get_test_name() or "Unknown")
        layout.addWidget(QLabel("Select test:"))
        layout.addWidget(combo)

        btns_layout = QHBoxLayout()
        run_btn = make_button("Run test")
        clear_btn = make_button("Clear")
        btns_layout.addWidget(run_btn)
        btns_layout.addWidget(clear_btn)
        layout.addLayout(btns_layout)

        for panel in panels:
            panel.hide()
            layout.addWidget(panel)

        group.setLayout(layout)
        group.combo = combo
        group.panels = panels

        clear_btn.clicked.connect(lambda _, p=panels: [panel.clear() or panel.hide() for panel in p])
        run_btn.clicked.connect(lambda _, g=group: self._run_selected_test(g))

        return group

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        self.list_widget.itemSelectionChanged.connect(self._update_selected_models)
        self.select_all_btn.clicked.connect(self.selector_widget.select_all)
        self.clear_selection_btn.clicked.connect(self.selector_widget.clear_selection)

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

    def _run_selected_test(self, group: QGroupBox) -> None:
        """Run selected panel in the group."""
        if not self._validate_test_run():
            return
        datasets = self.version_manager.datasets
        idx = group.combo.currentIndex()
        if 0 <= idx < len(group.panels):
            for pnl in group.panels:
                pnl.hide()
            panel = group.panels[idx]
            try:
                support_multivariate = getattr(panel, "support_multivariate", False)
                if support_multivariate:
                    samples = [datasets[name].dataframe for name in self.selected_models]
                else:
                    samples = [datasets[name].series for name in self.selected_models]
                    
                panel.evaluate(
                    samples=samples,
                    alpha=self.alpha_spinbox.value(),
                    is_independent=self.independence_checkbox.isChecked()
                )
                panel.show()
            except Exception as e:
                panel.clear()
                self.messanger.show_error("Test running error", str(e))

    def _validate_test_run(self) -> bool:
        """Validate that test can be run."""
        if not self.selected_models:
            self.messanger.show_error("Test running error", "Please select at least one dataset")
            return False
        return True