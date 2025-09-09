from typing import Any

# Controllers
from controllers import (
    AnomalyController, MissingDataController, DataTransformController,
    ParameterEstimation, SimulationController, StatisticController, GOFController, HomogenController,
    DataLoadController, DataVersionController,
    GraphController, UIStateController
)

# Services
from services import (
    TransformationService, AnomalyService, MissingService,
    ConfidenceService, TestPerformer, StatisticsService,
    UIRefreshService, UIMessager, MissingInfoDisplayService, TableRenderer,
    DataVersionManager, DataLoaderService,
    SimulationService, DataSaver
)

# Views
from PyQt6.QtWidgets import QTabWidget
from views import (
    # tabs
    DataProcessingTab, GOFTestTab, ParamEstimationTab, SimulationTab, StatisticTab, HomogenTab,
    # widgets
    WindowWidgets,
    AnomalyWidget, MissingWidget, TransformDataWidget,
    KolmogorovSmirnovPanel, PearsonChi2Panel,
    #...
    GraphPanel, DistributionSelector
)

# Callbacks
from callbacks import (
    UIClearCallbacks, UIModelCallbacks, UIStateCallbacks, UIUpdateCallbacks,
    build_dp_control_callbacks, build_combo_callbacks, build_graph_panel_callbacks
)


class ControllersFactory:
    def __init__(self, window, context):
        self.window = window
        self.context = context
    
    def init_controllers(self) -> dict[str, Any]:
        """Initialize all controllers with no UI dependencies"""
        controllers = {}
        
        controllers['statistic'] = StatisticController(
            context=self.context,
            statistic_service=StatisticsService()
        )
        controllers['graph'] = GraphController(
            context=self.context,
            confidence_service=ConfidenceService(),
        )
        controllers['ui_state'] = UIStateController(
            context=self.context,
            detect_missing_func=MissingService.detect_missing
        )
        controllers['data_loader'] = DataLoadController(
            context=self.context,
            loader_service=DataLoaderService(),
            select_file_callback=lambda: DataLoaderService.select_file(self.window),
            on_data_loaded_callback=lambda data: (controllers['ui_state'].handle_post_load_state(data))
        )
        controllers['simulation'] = SimulationController(
            simulation_service=SimulationService(TestPerformer()),
            data_saver=DataSaver(self.context, on_save=lambda data: controllers['ui_state'].handle_post_load_state(data))
        )
        controllers['estimation'] = ParameterEstimation()
        controllers['gof'] = GOFController()
        controllers['homogen'] = HomogenController()
        controllers['data_version'] = DataVersionController(context=self.context)
        controllers['anomaly_data'] = AnomalyController(
            context=self.context,
            anomaly_service=AnomalyService(),
        )
        controllers['data_transform'] = DataTransformController(
            context=self.context,
            transform_service=TransformationService()
        )
        controllers['missing_data'] = MissingDataController(
            context=self.context,
            missing_service=MissingService()
        )
        
        return controllers

class UIFactory:
    def __init__(self, window, context):
        self.window = window
        self.context = context
    
    def setup_ui(self, controllers: dict[str, Any]) -> None:
        # WINDOW WIDGETS
        self.window.widgets = WindowWidgets.create_controls_bar()

        # GRAPH PANEL
        self.window.graph_panel = GraphPanel(
            dist_selector_cls=DistributionSelector,
            graph_controller=controllers['graph'],
            get_data_model=lambda: self.context.data_model
        )

        # LEFT TABS
        data_tab = DataProcessingTab(
            widget_data=[
                ("transform_widget", TransformDataWidget, controllers['data_transform']),
                ("anomaly_widget", AnomalyWidget, controllers['anomaly_data']),
                ("missing_widget", MissingWidget, controllers['missing_data'])
            ],
            on_data_version_changed=controllers['data_version'].on_dataset_selection_changed,
            on_original_clicked=controllers['data_version'].revert_to_original,
            on_column_changed=controllers['data_version'].on_current_col_changed
        )
        stat_tab = StatisticTab(renderer_cls=TableRenderer)
        gof_tab = GOFTestTab(
            get_data_model=lambda: self.context.data_model,
            get_dist_func=lambda: self.window.graph_panel.get_selected_distribution(),
            gof_controller=controllers['gof'],
            test_panels=[PearsonChi2Panel, KolmogorovSmirnovPanel]
        )
        homo_tab = HomogenTab(
            get_data_model=lambda: self.context.data_model,
            homogen_controller = controllers['homogen'],
            homogen_panels=[]
        )
        sim_tab = SimulationTab(
            context=self.context,
            simulation_controller=controllers['simulation']
        )
        est_tab = ParamEstimationTab(
            context=self.context,
            estimator=controllers['estimation']
        )

        self.window.left_tab_widget = QTabWidget()
        self.window.left_tab_widget.addTab(data_tab, "Data Processing")
        self.window.left_tab_widget.addTab(stat_tab, "Statistic")
        self.window.left_tab_widget.addTab(gof_tab, "Goodness-of-Fit Tests")
        self.window.left_tab_widget.addTab(homo_tab, "Homogeneity Tests")
        self.window.left_tab_widget.addTab(sim_tab, "Simulation")
        self.window.left_tab_widget.addTab(est_tab, "Parameters estimation")
        # add to window attr
        self.window.data_tab = data_tab
        self.window.stat_tab = stat_tab
        self.window.gof_tab = gof_tab
        self.window.homo_tab = homo_tab
        self.window.sim_tab = sim_tab
        self.window.est_tab = est_tab

class ConnectFactory:
    def __init__(self, window):
        self.window = window

    def connect_ui(self, controllers):
        self.window.widgets.load_button.clicked.connect(controllers['data_loader'].load_data_file)
        self.window.widgets.precision_spinbox.valueChanged.connect(controllers['statistic'].update_statistics_table)

        controllers['data_version'].set_set_bins_value_func(lambda bins: self.window.graph_panel.bins_spinbox.setValue(bins))
        controllers['statistic'].connect_ui(
            stats_renderer=self.window.stat_tab.renderer,
            get_bins_value=lambda: self.window.graph_panel.bins_spinbox.value(),     
            get_confidence_value=lambda: self.window.graph_panel.confidence_spinbox.value(),         
            get_precision_value=lambda: self.window.widgets.precision_spinbox.value()
        )
        data_tab = self.window.data_tab
        controllers['anomaly_data'].set_get_gamma_value_func(data_tab.anomaly_widget.anomaly_gamma_spinbox.value)
        controllers['data_transform'].set_get_shift_value_func(lambda: data_tab.transform_widget.shift_spinbox.value())
        controllers['missing_data'].set_display_service(
            MissingInfoDisplayService(
                set_count_label=lambda text: data_tab.missing_widget.missing_count_label.setText(text),
                set_percent_label=lambda text: data_tab.missing_widget.missing_percentage_label.setText(text)
            )
        )

class CallBackFactory:
    def __init__(self, window, context):
        self.window = window
        self.context = context
    
    def connect_callbacks(self, controllers: dict[str, Any]) -> None:
        # set controller callbacks
        controllers['anomaly_data'].set_get_gamma_value_func(lambda: self.window.data_tab.anomaly_widget.anomaly_gamma_spinbox.value())
        controllers['data_transform'].set_on_transformation_applied_callback(lambda: self.window.data_tab.original_button.setEnabled(True))
        controllers['missing_data'].set_update_state_callback(controllers['ui_state'].update_state_for_data)

        controllers['graph'].connect_callbacks(
            graph_control=build_graph_panel_callbacks(self.window.graph_panel),
            update_statistics_callback=controllers['statistic'].update_statistics_table,
            update_gof_callback=self.window.gof_tab.evaluate_tests
        )
        controllers['ui_state'].connect_callbacks(
            ui_controls=build_dp_control_callbacks(self.window),
            enable_data_combo_callback=self.window.data_tab.data_version_combo.setEnabled,
            enable_col_combo_callback=self.window.data_tab.dataframe_cols_combo.setEnabled,
            update_data_callback=lambda data: controllers['missing_data'].update_data_reference(data),
            update_data_versions_callback=controllers['data_version'].update_dataset_list
        )
        controllers['data_version'].connect_callbacks(
            version_combo_controls=build_combo_callbacks(self.window.data_tab.data_version_combo),
            columns_combo_control=build_combo_callbacks(self.window.data_tab.dataframe_cols_combo),
            update_navigation_buttons=controllers['ui_state'].update_navigation_buttons,
            on_reverted_to_original=lambda: controllers['ui_state'].update_state_for_data(self.context.data_model.series),
            on_dataset_changed=lambda series: (
                controllers['missing_data'].update_data_reference(series),
                self.window.data_tab.dataframe_cols_combo.setEnabled(self.context.data_model.dataframe.shape[1] > 1)
            )
        )
        # set graph panel callbacks
        self.window.graph_panel.connect_controls()

        # set refresher
        self.context.refresher = UIRefreshService(
            clear=UIClearCallbacks(
                clear_graph=self.window.graph_panel.clear,
                clear_stats=controllers['statistic'].clear,
                clear_gof=self.window.gof_tab.clear_panels
            ),
            update=UIUpdateCallbacks(
            set_graph_data=lambda data: (controllers['graph'].set_data(data)),
            update_stats=controllers['statistic'].update_statistics_table,
            evaluate_gof=self.window.gof_tab.evaluate_tests
            ),
            state=UIStateCallbacks(
                update_state=controllers['ui_state'].update_state_for_data,
                update_transformation_label=controllers['ui_state'].update_transformation_label,
                update_navigation_buttons=controllers['ui_state'].update_navigation_buttons,
                enable_original_button=self.window.data_tab.original_button.setEnabled
            ),
            model=UIModelCallbacks(
                get_bins_count=lambda: self.window.graph_panel.bins_spinbox.value(),
                update_model_bins=lambda bins: self.context.data_model.update_bins(bins)
            )
        )

class Factory:
    def __init__(self, window, context):
        self.window = window
        self.context = context
        self.controllers: dict[str, Any] = {}

    @classmethod
    def create(cls, window, context):
        factory = cls(window, context)
        factory._setup_context()
        factory._init_controllers()
        factory._setup_ui()
        factory._connect_ui()
        factory._connect_callbacks()
        return factory

    def _setup_context(self):
        self.context.version_manager = DataVersionManager()
        self.context.messanger = UIMessager(parent=self.window)
        self.context.refresher = None
        self.context.data_model = None

    def _init_controllers(self):
        controllers_factory = ControllersFactory(self.window, self.context)
        self.controllers = controllers_factory.init_controllers()

    def _setup_ui(self):
        ui_factory = UIFactory(self.window, self.context)
        ui_factory.setup_ui(self.controllers)
    
    def _connect_ui(self):
        connect_factory = ConnectFactory(self.window)
        connect_factory.connect_ui(self.controllers)

    def _connect_callbacks(self):
        cb_factory = CallBackFactory(self.window, self.context)
        cb_factory.connect_callbacks(self.controllers)