from typing import Any

# Controllers
from controllers import (
    AnomalyController, MissingDataController, DataTransformController,
    ParameterEstimation, SimulationController, StatisticController,
    DataLoadController, DataVersionController,
    GraphController, UIStateController
)

# Services
from services import (
    TransformationService, AnomalyService, MissingService,
    ConfidenceService, GOFService, TestPerformer, StatisticsService,
    UIRefreshService, UIMessager, MissingInfoDisplayService, TableRenderer,
    DataVersionManager, DataLoaderService,
    SimulationService, DataSaver
)

# Views
from PyQt6.QtWidgets import QTabWidget
from views import (
    # tabs
    DataProcessingTab, GOFTestTab, ParamEstimationTab, SimulationTab, StatisticTab,
    # widgets
    WindowWidgets,
    AnomalyWidget, MissingWidget, ProcessDataWidget,
    KolmogorovSmirnovPanel, PearsonChi2Panel,
    GraphPanel, DistributionSelector
)

# Callbacks
from callbacks import (
    UIClearCallbacks, UIModelCallbacks, UIStateCallbacks, UIUpdateCallbacks,
    build_dp_control_callbacks, build_data_version_callbacks, build_graph_panel_callbacks
)


class ControllersFactory:
    def __init__(self, window, context):
        self.window = window
        self.context = context
    
    def init_controllers(self) -> dict[str, Any]:
        """Initialize all controllers with no UI dependencies"""
        controllers = {}
        
        controllers['estimation'] = ParameterEstimation()
        controllers['simulation'] = SimulationController(
            simulation_service=SimulationService(TestPerformer()),
            data_saver=DataSaver(self.context)
        )
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
        self.window.widgets = WindowWidgets(self.window)

        # GRAPH PANEL
        self.window.graph_panel = GraphPanel(
            dist_selector_cls=DistributionSelector
        )

        # LEFT TABS
        data_tab = DataProcessingTab(
            widgets_with_controllers=[
                (ProcessDataWidget, controllers['data_transform']),
                (AnomalyWidget, controllers['anomaly_data']),
                (MissingWidget, controllers['missing_data'])
            ],
            on_data_version_changed=controllers['data_version'].on_data_version_changed,
            on_original_clicked=controllers['data_version'].original_data
        )
        stat_tab = StatisticTab(renderer_cls=TableRenderer)
        gof_tab = GOFTestTab(
            context=self.context,
            get_dist_func=self.window.graph_panel.get_selected_distribution,
            gof_service=GOFService(),
            test_panels=[PearsonChi2Panel, KolmogorovSmirnovPanel]
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
        self.window.left_tab_widget.addTab(sim_tab, "Simulation")
        self.window.left_tab_widget.addTab(est_tab, "Parameters estimation")

class ConnectFactory:
    def __init__(self, window):
        self.window = window

    def connect_controllers(self, controllers):
        controllers['statistic'].connect_ui(
            stats_renderer=self.window.left_tab_widget.stat_tab.renderer,
            get_bins_value=..., 
            get_precision_value=..., 
            get_confidence_value=...           
        )
        controllers['data_version'].set_set_bins_value_func(set_bins_value=...)
        controllers['anomaly_data'].set_get_gamma_value_func(...)
        controllers['data_transform'].set_get_shift_value_func(...)
        controllers['missing_data'].set_display_service(...)

class CallBackFactory:
    def __init__(self, window, context):
        self.window = window
        self.context = context
    
    def connect_callbacks(self, controllers: dict[str, Any]) -> None:
        controllers['simulation'].data_saver.set_on_save_callback(...)
        controllers['missing_data'].set_update_state_callback(...)
        controllers['data_transform'].set_on_transformation_applied_callback(...)

        controllers['graph'].connect_callbacks(
            graph_control=...,
            update_statistics_callback=...,
            update_gof_callback=...
        )
        controllers['ui_state'].connect_callbacks(
            ui_controls=...,
            enable_data_combo_callback=...,
            update_data_callback=...,
            update_data_versions_callback=...
        )
        controllers['data_version'].connect_callbacks(
            version_combo_controls=...,
            update_navigation_buttons=...,
            on_reverted_to_original=...,
            on_version_changed=...
        )

        # set refresher
        self.context.refresher = UIRefreshService(
            clear=...,
            update=...,
            state=...,
            model=...            
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
        factory._connect_controllers()
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
    
    def _connect_controllers(self):
        connect_factory = ConnectFactory(self.window)
        connect_factory.connect_controllers(self.controllers)

    def _connect_callbacks(self):
        cb_factory = CallBackFactory(self.window, self.context)
        cb_factory.connect_callbacks(self.controllers)