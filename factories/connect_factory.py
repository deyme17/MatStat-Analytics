from .controllers_factory import Controllers
from utils import EventBus, EventType


class ConnectFactory:
    def __init__(self, window, event_bus: EventBus, controllers: Controllers):
        self.win = window
        self.event_bus = event_bus
        self.controllers = controllers

    def connect_ui(self) -> None:
        """Connect all UI components with corresponding controllers."""
        self._connect_window_controls()
        self._connect_data_version_controller()

    def _connect_window_controls(self) -> None:
        """Connect global controls bar events."""
        controls_bar = self.win.controls_bar
        controls_bar.on_load_clicked(self.controllers.data_loader.load_data_file)
        controls_bar.on_precision_changed(
            lambda value: self.event_bus.emit_type(EventType.PRECISION_CHANGED, value)
        )

    def _connect_data_version_controller(self) -> None:
        """Connect data version controller with dropdown controls."""
        data_tab = self.win.data_tab
        self.controllers.data_version.connect_ui(
            version_combo_control=data_tab.get_version_callbacks(),
            columns_combo_control=data_tab.get_columns_callbacks(),
        )