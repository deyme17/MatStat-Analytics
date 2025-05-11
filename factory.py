from controllers.data_transform_controller import DataTransformController
from controllers.data_version_controller import DataVersionController
from controllers.ui_state_controller import UIStateController
from controllers.anomaly_controller import AnomalyController
from controllers.missing_controller import MissingDataController
from controllers.statistic_controller import StatisticController

from services.data_history_manager import DataHistoryManager
from services.data_transformer import DataTransformer

class Factory:
    @staticmethod
    def create(window):
        # Services
        window.version_manager = DataHistoryManager()
        window.transform_manager = DataTransformer()

        # Controllers
        window.transform_controller = DataTransformController(window)
        window.data_version_controller = DataVersionController(window)
        window.state_controller = UIStateController(window)
        window.anomaly_controller = AnomalyController(window)
        window.missing_controller = MissingDataController(window)
        window.stat_controller = StatisticController(window)
