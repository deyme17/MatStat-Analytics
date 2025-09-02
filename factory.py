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
        controllers['anomaly'] = AnomalyController(
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
    
    def setup_ui(self) -> None:
        ...

class ConnectFactory:
    def __init__(self, window):
        self.window = window

    def connect_controllers(self, controllers):
        ...

class CallBackFactory:
    def __init__(self, window, context):
        self.window = window
        self.context = context
    
    def setup_callbacks(self) -> None:
        ...


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
        factory._setup_callbacks()
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
        ui_factory.setup_ui()
    
    def _connect_controllers(self):
        connect_factory = ConnectFactory(self.window)
        connect_factory.connect_controllers(self.controllers)

    def _setup_callbacks(self):
        cb_factory = CallBackFactory(self.window, self.context)
        cb_factory.setup_callbacks()