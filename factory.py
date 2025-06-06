from controllers.data_controllers.data_transform_controller import DataTransformController
from controllers.data_controllers.data_version_controller import DataVersionController
from controllers.data_controllers.data_loader import DataLoadController
from controllers.ui_controllers.ui_state_controller import UIStateController
from controllers.analysis_controller.anomaly_controller import AnomalyController
from controllers.analysis_controller.missing_controller import MissingDataController
from controllers.analysis_controller.statistic_controller import StatisticController
from controllers.ui_controllers.graph_controller import GraphController

from models.data_model import DataModel

from services.data_services.data_history_manager import DataHistoryManager
from services.data_services.data_loader_service import DataLoaderService
from services.analysis_services.missing_service import MissingService
from services.analysis_services.statistics_service import StatisticsService
from services.analysis_services.anomaly_service import AnomalyService
from services.data_services.transformation_service import TransformationService
from services.ui_services.ui_refresh_service import UIRefreshService

from views.widgets.statwidgets.graph_panel import GraphPanel


class Factory:
    @staticmethod
    def create(window):
        Factory._setup_services(window)
        Factory._setup_controllers(window)
        Factory._setup_graphics(window)

    @staticmethod
    def _setup_services(window):
        window.version_manager = DataHistoryManager()
        window.refresher = UIRefreshService()

    @staticmethod
    def _setup_controllers(window):
        window.data_load_controller = DataLoadController(window=window, data_model=DataModel, loader_service=DataLoaderService())
        window.transform_controller = DataTransformController(window=window, transform_service=TransformationService())
        window.data_version_controller = DataVersionController(window)
        window.state_controller = UIStateController(window)
        window.anomaly_controller = AnomalyController(window=window, anomaly_service=AnomalyService())
        window.missing_controller = MissingDataController(window=window, missing_service=MissingService())
        window.stat_controller = StatisticController(window=window, statistic_service=StatisticsService())

    @staticmethod
    def _setup_graphics(window):
        window.graph_panel = GraphPanel(window)
        window.graph_controller = GraphController(window.graph_panel)
        window.graph_panel.on_dist_change = lambda: window.graph_controller.evaluate_distribution_change()
