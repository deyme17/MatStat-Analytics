from typing import Any
from utils import EventBus, EventType, AppContext

# Controllers
from controllers import (
    AnomalyController, MissingDataController, DataTransformController,
    ParameterEstimation, SimulationController, StatisticController, GOFController, HomogenController,
    DataLoadController, DataVersionController
)

# Services
from services import (
    TransformationService, AnomalyService, MissingService,
    ConfidenceService, TestPerformer, StatisticsService,
    UIMessager, MissingInfoDisplayService, StatsRenderer, VarSerRenderer,
    DataVersionManager, DataLoaderService,
    SimulationService, DataSaver, DataExporter
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
    NormalHomogenPanel, WilcoxonPanel, MannWhitneyUPanel, RankMeanDiffPanel, SmirnovKolmogorovPanel, SignsCriterionPanel, AbbePanel,
    ANOVAPanel, BurtlettPanel, CochranQPanel, HPanel,
    GraphPanel, DistributionSelector
)
from views.widgets.statwidgets.graph_tabs import EDFTab, HistogramTab

# Callbacks
from utils.combo_callbacks import build_combo_callbacks


class ControllersFactory:
    def __init__(self, window, context: AppContext):
        self.window = window
        self.context: AppContext = context
    
    def init_controllers(self) -> dict[str, Any]:
        """Initialize all controllers with no UI dependencies"""
        controllers = {}
        
        controllers['statistic'] = StatisticController(
            context=self.context,
            statistic_service=StatisticsService()
        )
        controllers['data_loader'] = DataLoadController(
            context=self.context,
            loader_service=DataLoaderService(),
            select_file_callback=lambda: DataLoaderService.select_file(self.window)
        )
        controllers['simulation'] = SimulationController(
            context=self.context,
            simulation_service=SimulationService(TestPerformer()),
            data_saver=DataSaver(),
            data_exporter=DataExporter
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
    def __init__(self, window, context: AppContext):
        self.window = window
        self.context: AppContext = context
    
    def setup_ui(self, controllers: dict[str, Any]) -> None:
        # WINDOW WIDGETS
        self.window.widgets = WindowWidgets.create_controls_bar()

        # GRAPH PANEL
        self.window.graph_panel = GraphPanel(
            context=self.context,
            dist_selector_cls=DistributionSelector,
            graph_tabs={
                "Histogram": HistogramTab(self.context),
                "EDF": EDFTab(self.context, ConfidenceService()),
            }
        )

        # LEFT TABS
        data_tab = DataProcessingTab(
            context=self.context,
            widget_data=[
                ("transform_widget", TransformDataWidget, controllers['data_transform']),
                ("anomaly_widget", AnomalyWidget, controllers['anomaly_data']),
                ("missing_widget", MissingWidget, controllers['missing_data'])
            ]
        )
        stat_tab = StatisticTab(stat_renderer_cls=StatsRenderer, var_rendere_cls=VarSerRenderer)
        gof_tab = GOFTestTab(
            context=self.context,
            get_dist_func=lambda: self.window.graph_panel.get_selected_distribution(),
            gof_controller=controllers['gof'],
            test_panels=[PearsonChi2Panel, KolmogorovSmirnovPanel]
        )
        homo_tab = HomogenTab(
            homogen_controller=controllers['homogen'],
            context=self.context,
            homogen_2samples_panels=[NormalHomogenPanel, WilcoxonPanel, MannWhitneyUPanel, 
                                     RankMeanDiffPanel, SmirnovKolmogorovPanel, SignsCriterionPanel],
            homogen_Nsamples_panels=[ANOVAPanel, BurtlettPanel, CochranQPanel, HPanel],
            hamogen_1sample_panels=[AbbePanel]
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
    def __init__(self, window, event_bus: EventBus):
        self.window = window
        self.event_bus: EventBus = event_bus

    def connect_ui(self, controllers):
        self.window.widgets.load_button.clicked.connect(lambda: controllers['data_loader'].load_data_file())
        self.window.widgets.precision_spinbox.valueChanged.connect(lambda: self.event_bus.emit_type(EventType.PRECISION_CHANGED))

        controllers['statistic'].connect_ui(
            stats_renderer=self.window.stat_tab.stat_renderer,
            var_renderer=self.window.stat_tab.var_renderer,
            get_bins_value=self.window.graph_panel.bins_spinbox.value,     
            get_confidence_value=self.window.graph_panel.confidence_spinbox.value,         
            get_precision_value=self.window.widgets.precision_spinbox.value
        )

        data_tab = self.window.data_tab

        controllers['data_version'].connect_ui(
            version_combo_controls=build_combo_callbacks(data_tab.data_version_combo),
            columns_combo_control=build_combo_callbacks(data_tab.dataframe_cols_combo),
            set_bins_value=lambda bins: self.window.graph_panel.bins_spinbox.setValue(bins)
        )
        controllers['anomaly_data'].connect_ui(data_tab.anomaly_widget.anomaly_gamma_spinbox.value)
        controllers['data_transform'].connect_ui(data_tab.transform_widget.shift_spinbox.value)
        controllers['missing_data'].connect_ui(
            MissingInfoDisplayService(
                set_count_label=lambda text: data_tab.missing_widget.missing_count_label.setText(text),
                set_percent_label=lambda text: data_tab.missing_widget.missing_percentage_label.setText(text)
            )
        )


class Factory:
    def __init__(self, window, context: AppContext):
        self.window = window
        self.context: AppContext = context
        self.controllers: dict[str, Any] = {}

    @classmethod
    def create(cls, window, context: AppContext):
        factory = cls(window, context)
        factory._setup_context()
        factory._init_controllers()
        factory._setup_ui()
        factory._connect_ui()
        return factory

    def _setup_context(self):
        self.context.version_manager = DataVersionManager()
        self.context.messanger = UIMessager(parent=self.window)
        self.context.event_bus = EventBus()
        self.context.data_model = None

    def _init_controllers(self):
        controllers_factory = ControllersFactory(self.window, self.context)
        self.controllers = controllers_factory.init_controllers()

    def _setup_ui(self):
        ui_factory = UIFactory(self.window, self.context)
        ui_factory.setup_ui(self.controllers)
    
    def _connect_ui(self):
        connect_factory = ConnectFactory(self.window, self.context.event_bus)
        connect_factory.connect_ui(self.controllers)