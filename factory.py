from controllers.data_controllers.data_transform_controller import DataTransformController
from controllers.data_controllers.data_version_controller import DataVersionController
from controllers.ui_controllers.ui_state_controller import UIStateController
from controllers.analysis_controller.anomaly_controller import AnomalyController
from controllers.analysis_controller.missing_controller import MissingDataController
from controllers.analysis_controller.statistic_controller import StatisticController
from controllers.ui_controllers.graph_controller import GraphController

from services.data_services.data_history_manager import DataHistoryManager
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

    @staticmethod
    def _setup_controllers(window):
        window.transform_controller = DataTransformController(window)
        window.data_version_controller = DataVersionController(window)
        window.state_controller = UIStateController(window)
        window.anomaly_controller = AnomalyController(window)
        window.missing_controller = MissingDataController(window)
        window.stat_controller = StatisticController(window)

    @staticmethod
    def _setup_graphics(window):
        window.graph_panel = GraphPanel(window)
        window.graph_controller = GraphController(window.graph_panel)
        window.graph_panel.on_dist_change = lambda: window.graph_controller.evaluate_distribution_change()
