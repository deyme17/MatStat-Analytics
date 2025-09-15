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
    """
    A tab widget for evaluating Homogeneity tests.
    """
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
        
        # test panels
        self.homogen_2samples_panels: list[BaseHomoTestPanel] = [panel(homogen_controller, self.messanger) for panel in homogen_2samples_panels]
        self.homogen_Nsamples_panels: list[BaseHomoTestPanel] = [panel(homogen_controller, self.messanger) for panel in homogen_Nsamples_panels]
        self.independence_panels: list[BaseHomoTestPanel] = [panel(homogen_controller, self.messanger) for panel in independence_panels]
        
        self.selected_models = []

        self.two_samples_combo = None
        self.n_samples_combo = None
        self.independence_combo = None
        
        # ui
        self._setup_ui()
        self._connect_signals()
        self.refresh_data_list()

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        self.setStyleSheet(groupStyle + groupMargin)
        main_layout = QVBoxLayout()
        
        # alpha section
        alpha_layout = self._create_alpha_spinbox()
        main_layout.addLayout(alpha_layout)

        # data selection section
        data_group = self._create_data_selection_section()
        main_layout.addWidget(data_group)
        
        # test sections
        tests_layout = QVBoxLayout()
        
        # two samples tests
        two_samples_group, self.two_samples_combo = self._create_test_section(
            "Homogeneity tests for two samples", 
            self.homogen_2samples_panels,
            self._run_2samples_test
        )
        tests_layout.addWidget(two_samples_group)
        # n samples tests  
        n_samples_group, self.n_samples_combo = self._create_test_section(
            "Homogeneity tests for multiple samples",
            self.homogen_Nsamples_panels, 
            self._run_nsamples_test
        )
        tests_layout.addWidget(n_samples_group)
        # independence tests
        independence_group, self.independence_combo = self._create_test_section(
            "Tests of independence of observations",
            self.independence_panels,
            self._run_independence_test
        )
        tests_layout.addWidget(independence_group)
        
        main_layout.addLayout(tests_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def _create_alpha_spinbox(self) -> QHBoxLayout:
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

    def _create_data_selection_section(self) -> QGroupBox:
        """Create data selection section."""
        group = QGroupBox("Select datasets for testing")
        layout = QVBoxLayout()
        
        # datasets list
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.list_widget.setMaximumHeight(LIST_WIDGET_HEIGHT)
        self.list_widget.setMaximumWidth(LIST_WIDGET_WIDTH)
        
        # buttons
        buttons_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("Select ALL")
        self.clear_selection_btn = QPushButton("Clear selection")
        
        buttons_layout.addWidget(self.select_all_btn)
        buttons_layout.addWidget(self.clear_selection_btn)
        
        # count label
        self.selected_count_label = QLabel("Selected: 0 datasets")

        # independence checkbox
        self.independence_checkbox = QCheckBox("Samples are independent")
        self.independence_checkbox.setChecked(False)
        
        layout.addWidget(self.list_widget)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.selected_count_label)
        layout.addWidget(self.independence_checkbox)
        
        group.setLayout(layout)
        group.setMaximumHeight(150)
        return group

    def _create_test_section(self, title: str, panels: list[BaseHomoTestPanel], 
                           run_callback) -> tuple[QGroupBox, QComboBox]:
        """Create a test section with panels and run button."""
        group = QGroupBox(title)
        layout = QVBoxLayout()
        
        # test selection combo box
        test_label = QLabel("Select test:")
        combo_box = QComboBox()
        for panel in panels:
            test_name = panel.get_test_name() or "Uknowm"
            combo_box.addItem(test_name)
        
        if not panels:
            combo_box.addItem("No tests available")
            combo_box.setEnabled(False)
        
        layout.addWidget(test_label)
        layout.addWidget(combo_box)
        
        # run selected test button
        run_btn = QPushButton("Run test")
        run_btn.clicked.connect(run_callback)
        if not panels:
            run_btn.setEnabled(False)
        
        layout.addWidget(run_btn)
        layout.addStretch()
        
        group.setLayout(layout)
        return group, combo_box

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        self.list_widget.itemSelectionChanged.connect(self._update_selected_models)
        self.select_all_btn.clicked.connect(self._select_all)
        self.clear_selection_btn.clicked.connect(self._clear_selection)

    def refresh_data_list(self) -> None:
        """Refresh the data models list."""
        self.list_widget.clear()
        data_models = self.get_data_models()
        if data_models:
            for name, model in data_models.items():
                if model.series is not None and not model.series.empty:
                    self.list_widget.addItem(name)

    def _update_selected_models(self) -> None:
        """Update selected models list and label."""
        selected_items = self.list_widget.selectedItems()
        self.selected_models = [item.text() for item in selected_items]
        count = len(self.selected_models)
        self.selected_count_label.setText(f"Selected: {count} datasets")

    def _select_all(self) -> None:
        """Select all items in the list."""
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setSelected(True)

    def _clear_selection(self) -> None:
        """Clear all selections."""
        self.list_widget.clearSelection()

    def _run_selected_test(self, panels: list[BaseHomoTestPanel], combo: QComboBox, run_method) -> None:
        """Run the selected test from given panels using provided controller method."""
        if not self._validate_test_run():
            return

        selected_index = combo.currentIndex()
        if 0 <= selected_index < len(panels):
            selected_panel = panels[selected_index]
            alpha = self.alpha_spinbox.value()

            run_method(
                selected_models=self.selected_models,
                alpha=alpha,
                is_independent=self.independence_checkbox.isChecked(),
                test_panel=selected_panel
            )
    def _run_2samples_test(self) -> None:
        self._run_selected_test(
            self.homogen_2samples_panels, 
            self.two_samples_combo,
            self.homogen_controller.run_2samples_test
        )
    def _run_nsamples_test(self) -> None:
        self._run_selected_test(
            self.homogen_Nsamples_panels,
            self.n_samples_combo,
            self.homogen_controller.run_Nsamples_test
        )
    def _run_independence_test(self) -> None:
        self._run_selected_test(
            self.independence_panels,
            self.independence_combo,
            self.homogen_controller.run_independence_test
        )

    def _validate_test_run(self) -> bool:
        """Validate that test can be run."""
        if len(self.selected_models) < 1:
            self.messanger.show_error("Test running error", "Please select at least one dataset")
            return False
        return True