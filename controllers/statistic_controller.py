from services.statistics_service import StatisticsService
from models.graph_model.hist_models import Hist

class StatisticController:
    def __init__(self, window):
        self.window = window

    def update_statistics_table(self):
        data = self.window.data
        if data is None or data.empty:
            return

        bins = self.window.graph_panel.bins_spinbox.value()
        hist_model = Hist(data, bins=bins)

        confidence = self.window.graph_panel.confidence_spinbox.value()

        StatisticsService.update_table(
            self.window.stat_tab.conf_table,
            hist_model,
            data,
            precision=self.window.precision_spinbox.value(),
            confidence_level=confidence
        )
