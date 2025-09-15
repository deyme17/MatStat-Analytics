from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
    QPushButton, QAbstractItemView, QLabel, QDoubleSpinBox, 
    QGroupBox, QComboBox, QCheckBox
)
from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel
from utils.ui_styles import groupMargin, groupStyle

ALPHA_MIN, ALPHA_MAX = 0.01, 0.99
ALPHA_STEP = 0.01
ALPHA_PRECISION = 2
DEFAULT_ALPHA = 0.05

LIST_WIDGET_HEIGHT = 150
LIST_WIDGET_WIDTH = 320


class HomogenTab(QWidget):
    """Tab widget for homogeneity tests."""
    def __init__(self, get_data_models, homogen_controller, messanger,
                 homogen_2samples_panels: list[BaseHomoTestPanel],
                 homogen_Nsamples_panels: list[BaseHomoTestPanel],
                 independence_panels: list[BaseHomoTestPanel]) -> None:
        """
        Args:
            get_data_models: Function for getting all data models (dict[str, DataModel]).
            homogen_controller (HomogenController): Controller to perform Homogeneity tests.
            messanger: Service for sending message to user
            homogen_2samples_panels (list): List of Homogeneity test panel classes for two samples test.
            homogen_Nsamples_panels (list): List of Homogeneity test panel classes for N samples test.
            independence_panels (list): List of Independence test panel classes.
        """
        super().__init__()
        self.get_data_models = get_data_models
        self.homogen_controller = homogen_controller
        self.messanger = messanger
        self.selected_models = []

        # panels
        self.two_samples_panels = [pnl(homogen_controller) for pnl in homogen_2samples_panels]
        self.n_samples_panels = [pnl(homogen_controller) for pnl in homogen_Nsamples_panels]
        self.independence_panels = [pnl(homogen_controller) for pnl in independence_panels]

        self._setup_ui()
        self._connect_signals()
        self.refresh_data_list()

    def _setup_ui(self):
        """Setup the user interface."""
        self.setStyleSheet(groupStyle + groupMargin)
        main_layout = QVBoxLayout()
        main_layout.addLayout(self._create_alpha_spinbox())
        main_layout.addWidget(self._create_data_selection_section())

        # test sections
        main_layout.addWidget(self._create_test_section("Homogeneity tests for two samples", self.two_samples_panels))
        main_layout.addWidget(self._create_test_section("Homogeneity tests for multiple samples", self.n_samples_panels))
        main_layout.addWidget(self._create_test_section("Tests of independence of observations", self.independence_panels))

        main_layout.addStretch()
        self.setLayout(main_layout)

    def _create_alpha_spinbox(self):
        """Create alpha parameter selection section."""
        layout = QHBoxLayout()
        self.alpha_spinbox = QDoubleSpinBox()
        self.alpha_spinbox.setRange(ALPHA_MIN, ALPHA_MAX)
        self.alpha_spinbox.setSingleStep(ALPHA_STEP)
        self.alpha_spinbox.setDecimals(ALPHA_PRECISION)
        self.alpha_spinbox.setValue(DEFAULT_ALPHA)
        layout.addWidget(QLabel("Significance level α:"))
        layout.addWidget(self.alpha_spinbox)
        layout.addStretch()
        return layout

    def _create_data_selection_section(self):
        """Create data selection section."""
        group = QGroupBox("Select datasets for testing")
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.list_widget.setMaximumHeight(LIST_WIDGET_HEIGHT)
        self.list_widget.setMaximumWidth(LIST_WIDGET_WIDTH)

        btns_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("Select ALL")
        self.clear_selection_btn = QPushButton("Clear selection")
        btns_layout.addWidget(self.select_all_btn)
        btns_layout.addWidget(self.clear_selection_btn)

        self.selected_count_label = QLabel("Selected: 0 datasets")
        self.independence_checkbox = QCheckBox("Samples are independent")
        self.independence_checkbox.setChecked(False)

        layout.addWidget(self.list_widget)
        layout.addLayout(btns_layout)
        layout.addWidget(self.selected_count_label)
        layout.addWidget(self.independence_checkbox)

        group.setLayout(layout)
        group.setMaximumHeight(150)
        return group

    def _create_test_section(self, title: str, panels: list[BaseHomoTestPanel]):
        """Create a test section with panels, run button, and clear button."""
        group = QGroupBox(title)
        layout = QVBoxLayout()

        combo = QComboBox()
        for panel in panels:
            combo.addItem(panel.get_test_name() or "Unknown")
        layout.addWidget(QLabel("Select test:"))
        layout.addWidget(combo)

        btns_layout = QHBoxLayout()
        run_btn = QPushButton("Run test")
        clear_btn = QPushButton("Clear")
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

    def _connect_signals(self):
        """Connect UI signals."""
        self.list_widget.itemSelectionChanged.connect(self._update_selected_models)
        self.select_all_btn.clicked.connect(lambda: [self.list_widget.item(i).setSelected(True) for i in range(self.list_widget.count())])
        self.clear_selection_btn.clicked.connect(self.list_widget.clearSelection)

    def refresh_data_list(self):
        """Refresh the data models list."""
        self.list_widget.clear()
        for name, model in (self.get_data_models() or {}).items():
            if model.series is not None and not model.series.empty:
                self.list_widget.addItem(name)

    def _update_selected_models(self):
        """Update selected models list and label."""
        self.selected_models = [item.text() for item in self.list_widget.selectedItems()]
        self.selected_count_label.setText(f"Selected: {len(self.selected_models)} datasets")

    def _run_selected_test(self, group: QGroupBox):
        """Run selected panel in the group."""
        if not self._validate_test_run():
            return
        idx = group.combo.currentIndex()
        if 0 <= idx < len(group.panels):
            panel = group.panels[idx]
            panel.evaluate(
                samples=self.selected_models,
                alpha=self.alpha_spinbox.value(),
                is_independent=self.independence_checkbox.isChecked()
            )
            panel.show()

    def _validate_test_run(self):
        """Validate that test can be run."""
        if not self.selected_models:
            self.messanger.show_error("Test running error", "Please select at least one dataset")
            return False
        return True