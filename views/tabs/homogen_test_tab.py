from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
    QPushButton, QAbstractItemView, QLabel, QDoubleSpinBox, 
    QGroupBox
)
from views.widgets.homogenwidgets.homogen_panel import BaseHomoTestPanel
from utils.ui_styles import groupMargin, groupStyle

ALPHA_MIN, ALPHA_MAX = 0.01, 0.99
ALPHA_STEP = 0.01
ALPHA_PRECISION = 2
DEFAULT_ALPHA = 0.05

LIST_WIDGET_HEIGHT = 50
LIST_WIDGET_WIDTH = 320


class HomogenTab(QWidget):
    """
    A tab widget for evaluating Homogeneity tests.
    """
    def __init__(self, get_data_models, homogen_controller, 
                 homogen_2samples_panels: list[BaseHomoTestPanel],
                 homogen_Nsamples_panels: list[BaseHomoTestPanel],
                 independence_panels: list[BaseHomoTestPanel]) -> None:
        """
        Args:
            get_data_models: Function for getting all data models (dict[str, DataModel]).
            homogen_controller (HomogenController): Controller to perform Homogeneity tests.
            homogen_2samples_panels (list): List of Homogeneity test panel classes for two samples test.
            homogen_Nsamples_panels (list): List of Homogeneity test panel classes for N samples test.
            independence_panels (list): List of Independence test panel classes.
        """
        super().__init__()
        self.get_data_models = get_data_models
        self.homogen_controller = homogen_controller
        
        # test panels
        self.homogen_2samples_panels: list[BaseHomoTestPanel] = [panel(homogen_controller) for panel in homogen_2samples_panels]
        self.homogen_Nsamples_panels: list[BaseHomoTestPanel] = [panel(homogen_controller) for panel in homogen_Nsamples_panels]
        self.independence_panels: list[BaseHomoTestPanel] = [panel(homogen_controller) for panel in independence_panels]
        
        self.selected_models = []
        
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
        tests_layout = QHBoxLayout()
        
        # # Two samples tests
        # two_samples_group = self._create_test_section(
        #     "Homogeneity tests for two samples", 
        #     self.homogen_2samples_panels,
        #     self.run_2samples_tests
        # )
        # tests_layout.addWidget(two_samples_group)
        
        # # N samples tests  
        # n_samples_group = self._create_test_section(
        #     "Homogeneity tests for multiple samples",
        #     self.homogen_Nsamples_panels, 
        #     self.run_Nsamples_tests
        # )
        # tests_layout.addWidget(n_samples_group)
        
        # # Independence tests
        # independence_group = self._create_test_section(
        #     "Tests of independence of observations",
        #     self.independence_panels,
        #     self.run_independence_tests
        # )
        # tests_layout.addWidget(independence_group)
        
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
        self.refresh_btn = QPushButton("Update datasets")
        
        buttons_layout.addWidget(self.select_all_btn)
        buttons_layout.addWidget(self.clear_selection_btn)
        buttons_layout.addWidget(self.refresh_btn)
        
        # count label
        self.selected_count_label = QLabel("Selected: 0 datasets")
        
        layout.addWidget(self.list_widget)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.selected_count_label)
        
        group.setLayout(layout)
        group.setMaximumHeight(100)
        return group

    def _create_test_section(self, title: str, panels: list[BaseHomoTestPanel], 
                           run_callback) -> QGroupBox:
        """Create a test section with panels and run button."""
        group = QGroupBox(title)
        layout = QVBoxLayout()
        
        # add combo box for test selection
        # ...
        
        # Run button
        run_btn = QPushButton("Run test")
        run_btn.clicked.connect(run_callback)
        layout.addWidget(run_btn)
        
        layout.addStretch()
        group.setLayout(layout)
        return group

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        self.list_widget.itemSelectionChanged.connect(self._update_selected_models)
        self.select_all_btn.clicked.connect(self._select_all)
        self.clear_selection_btn.clicked.connect(self._clear_selection)
        self.refresh_btn.clicked.connect(self.refresh_data_list)

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

    def run_2samples_tests(self):
        pass

    def run_Nsamples_tests(self):
        pass

    def run_independence_tests(self):
        pass