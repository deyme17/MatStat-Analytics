from .base_dp_widget import BaseDataWidget
from PyQt6.QtWidgets import QLabel
from controllers import MissingDataController
from utils import EventBus, EventType, Event


class MissingWidget(BaseDataWidget):
    """Widget for handling missing data in the dataset."""
    def __init__(self, controller: MissingDataController, event_bus: EventBus):
        buttons_config = [
            ("impute_mean_button", "Replace with Mean",
             controller.impute_with_mean),
            ("impute_median_button", "Replace with Median",
             controller.impute_with_median),
            ("interpolate_linear_button", "Interpolate (Linear)",
             lambda: controller.interpolate_missing("linear")),
            ("drop_missing_button", "Drop Missing Values",
             controller.drop_missing_values)
        ]
        super().__init__("Missing Data", controller, event_bus, buttons_config)
        self._setup_missing_info()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.MISSING_VALUES_DETECTED, self._unable_widget)
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._disable_widget)
        self.event_bus.subscribe(EventType.MISSING_VALUES_INFO, self._on_missing_info)

    def _setup_missing_info(self) -> None:
        self.missing_count_label = QLabel("Total Missing: 0")
        self.missing_percentage_label = QLabel("Missing Percentage: 0.00%")
        self.add_widget(self.missing_count_label)
        self.add_widget(self.missing_percentage_label)

    def _on_missing_info(self, event: Event) -> None:
        info = event.data or {}
        count = info.get("total_missing", 0)
        pct   = info.get("missing_percentage", 0.0)
        self.missing_count_label.setText(f"Total Missing: {count}")
        self.missing_percentage_label.setText(f"Missing Percentage: {pct:.2f}%")