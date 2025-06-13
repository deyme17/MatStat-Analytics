# Controllers
from controllers.analysis_controller.anomaly_controller import AnomalyController
from controllers.analysis_controller.estimation_controller import ParameterEstimation
from controllers.analysis_controller.missing_controller import MissingDataController
from controllers.analysis_controller.simulation_controller import SimulationController
from controllers.analysis_controller.statistic_controller import StatisticController
from controllers.data_controllers.data_loader import DataLoadController
from controllers.data_controllers.data_transform_controller import DataTransformController
from controllers.data_controllers.data_version_controller import DataVersionController
from controllers.ui_controllers.graph_controller import GraphController
from controllers.ui_controllers.ui_state_controller import UIStateController

# Services
from services.analysis_services.confidence_assesment import ConfidenceService
from services.analysis_services.gof_register import GOFService
from services.analysis_services.stat_tests import TestPerformer
from services.analysis_services.statistics_service import StatisticsService
from services.data_services.data_history_manager import DataHistoryManager
from services.data_services.data_loader_service import DataLoaderService
from services.data_services.transformation_service import TransformationService
from services.preprocessing_services.anomaly_service import AnomalyService
from services.preprocessing_services.missing_service import MissingService
from services.simulation.simulation_engine import SimulationService
from services.simulation.simulation_saver import DataSaver
from services.ui_services.renderers.stats_renderer import TableRenderer
from services.ui_services.ui_refresh_service import UIRefreshService

# Views - Tabs
from PyQt6.QtWidgets import QTabWidget
from views.tabs.data_processing_tab import DataProcessingTab
from views.tabs.gof_test_tab import GOFTestTab
from views.tabs.params_estimation_tab import ParamEstimationTab
from views.tabs.simulation_tab import SimulationTab
from views.tabs.stat_table_tab import StatisticTab

# Views - Widgets
from views.widgets.window_widget import WindowWidgets
from views.widgets.dpwidgets.anomalywidget import AnomalyWidget
from views.widgets.dpwidgets.missingwidget import MissingWidget
from views.widgets.dpwidgets.processdatawidget import ProcessDataWidget
from views.widgets.hypoteswidgets.ks_panel import KolmogorovSmirnovPanel
from views.widgets.hypoteswidgets.pearson_panel import PearsonChi2Panel
from views.widgets.statwidgets.graph_panel import GraphPanel
from views.widgets.statwidgets.stat_dist_selector import DistributionSelector


class Factory:
    @staticmethod
    def create(window):
        Factory._setup_services(window)
        Factory._setup_controllers(window)
        Factory._setup_graphics(window)
        Factory._setup_tabs(window)

    @staticmethod
    def _setup_services(window):
        window.version_manager = DataHistoryManager()
        window.refresher = UIRefreshService(window)

    @staticmethod
    def _setup_controllers(window):
        window.data_load_controller = DataLoadController(
                                        window=window, 
                                        loader_service=DataLoaderService()
                                        )
        window.transform_controller = DataTransformController(
                                        window=window, 
                                        transform_service=TransformationService()
                                        )
        window.data_version_controller = DataVersionController(window)

        window.missing_controller = MissingDataController(
                                        window=window, 
                                        missing_service=MissingService()
                                        )
        window.anomaly_controller = AnomalyController(
                                        window=window, 
                                        anomaly_service=AnomalyService()
                                        )
        window.stat_controller = StatisticController(
                                        window=window, 
                                        statistic_service=StatisticsService(),
                                        stats_renderer=TableRenderer()
                                        )
        window.state_controller = UIStateController(
                                        window=window, 
                                        missing_service=MissingService()
                                        )

    @staticmethod
    def _setup_graphics(window):
        window.graph_controller = GraphController(
                                        window=window, 
                                        confidence_service=ConfidenceService()
                                        ) 
        
        graph_panel = GraphPanel(window, dist_selector=DistributionSelector)

        window.graph_panel = graph_panel
        window.graph_controller.panel = graph_panel

    @staticmethod
    def _setup_tabs(window):
        window.widgets = WindowWidgets(window)

        window.data_tab = DataProcessingTab(
            window,
            processor_widget=ProcessDataWidget,
            anomaly_widget=AnomalyWidget,
            missing_widget=MissingWidget
        )

        window.stat_tab = StatisticTab()

        window.gof_tab = GOFTestTab(
            window,
            gof_service=GOFService(),
            test_panels=[PearsonChi2Panel, KolmogorovSmirnovPanel]
        )

        window.sim_tab = SimulationTab(
            window,
            simulation_controller=SimulationController(
                simulation_service=SimulationService(test_performer=TestPerformer()),
                data_saver=DataSaver(window)
            )
        )

        window.est_tab = ParamEstimationTab(
            window,
            estimator=ParameterEstimation()
        )

        window.left_tab_widget = QTabWidget()
        window.left_tab_widget.addTab(window.data_tab, "Data Processing")
        window.left_tab_widget.addTab(window.stat_tab, "Statistic")
        window.left_tab_widget.addTab(window.gof_tab, "Goodness-of-Fit Tests")
        window.left_tab_widget.addTab(window.sim_tab, "Simulation")
        window.left_tab_widget.addTab(window.est_tab, "Parameters estimation")
