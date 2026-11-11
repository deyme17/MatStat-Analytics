from typing import Callable
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout
from utils.ui_styles import groupStyle
from utils import EventBus, Event
from views.widgets.utils import make_button


class BaseDataWidget(QGroupBox):
    """Base class for all data processing widgets."""
    def __init__(self, title: str, controller, event_bus: EventBus, buttons_config: list[tuple[str, str, Callable]]):
        super().__init__(title)
        self.controller = controller
        self.event_bus: EventBus = event_bus
        self.buttons_config = buttons_config
        self.setStyleSheet(groupStyle)
        
        self._layout = QVBoxLayout(self)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize button components from configuration list."""        
        for attr_name, text, callback in self.buttons_config:
            button = make_button(text, callback=callback, enabled=False)
            setattr(self, attr_name, button)
            self.add_widget(button)
        
    def add_widget(self, widget) -> None:
        """Add child widget to the layout."""
        self._layout.addWidget(widget)
        
    def add_layout(self, layout) -> None:
        """Add inner layout to the main layout."""
        self._layout.addLayout(layout)

    def _set_widget_status(self, enable: bool) -> None:
        """Set enablement state for all registered buttons."""
        for attr_name, _, _ in self.buttons_config:
            button = getattr(self, attr_name)
            button.setEnabled(enable)

    def _disable_widget(self, event: Event) -> None:
        """Disable all interactive buttons in widget."""
        self._set_widget_status(False)

    def _enable_widget(self, event: Event) -> None:
        """Enable all interactive buttons in widget."""
        self._set_widget_status(True)