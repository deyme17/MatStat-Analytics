from .controllers_factory import Controllers
from utils import EventBus, EventType
from utils.callbacks import build_combo_callbacks


class ConnectFactory:
    def __init__(self, window, event_bus: EventBus, controllers: Controllers):
        self.win = window
        self.event_bus = event_bus
        self.ctrl = controllers

    def connect_ui(self) -> None:
        self.win.widgets.load_button.clicked.connect(lambda: self.ctrl.data_loader.load_data_file())
        self.win.widgets.precision_spinbox.valueChanged.connect(self._on_precision_changed)

        self.ctrl.statistics.connect_ui(
            stats_renderer=self.win.stat_tab.stat_renderer,
            var_renderer=self.win.stat_tab.var_renderer,
            multi_renderer=self.win.stat_tab.multi_renderer,
            get_bins_value=self.win.graph_panel.bins_spinbox.value,
            get_confidence_value=self.win.graph_panel.confidence_spinbox.value,
            get_precision_value=self.win.widgets.precision_spinbox.value,
        )

        self.ctrl.data_version.connect_ui(
            version_combo_controls=build_combo_callbacks(self.win.data_tab.data_version_combo),
            columns_combo_control=build_combo_callbacks(self.win.data_tab.dataframe_cols_combo),
            set_bins_value=self.win.graph_panel.bins_spinbox.setValue,
        )

    def _on_precision_changed(self) -> None:
        self.event_bus.emit_type(EventType.PRECISION_CHANGED)