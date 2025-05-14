from controllers.data_controllers.data_transform_controller import DataTransformController
from controllers.data_controllers.data_version_controller import DataVersionController
from controllers.ui_controllers.ui_state_controller import UIStateController
from controllers.analysis_controller.anomaly_controller import AnomalyController
from controllers.analysis_controller.missing_controller import MissingDataController
from controllers.analysis_controller.statistic_controller import StatisticController

from services.data_services.data_history_manager import DataHistoryManager


class Factory:
    @staticmethod
    def create(window):
        # Services
        window.version_manager = DataHistoryManager()

        # Controllers
        window.transform_controller = DataTransformController(window)
        window.data_version_controller = DataVersionController(window)
        window.state_controller = UIStateController(window)
        window.anomaly_controller = AnomalyController(window)
        window.missing_controller = MissingDataController(window)
        window.stat_controller = StatisticController(window)
