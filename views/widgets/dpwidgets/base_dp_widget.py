from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QPushButton
from typing import Tuple, Callable, List
from utils.ui_styles import groupStyle
from utils import EventBus, Event

class BaseDataWidget(QGroupBox):
    """Base class for all data processing widgets."""
    def __init__(self, title, controller, event_bus: EventBus, buttons_config: List[Tuple[str, str, Callable]]):
        super().__init__(title)
        self.controller = controller
        self.event_bus: EventBus = event_bus
        self.buttons_config = buttons_config
        self.setStyleSheet(groupStyle)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""        
        for attr_name, text, callback in self.buttons_config:
            button = QPushButton(text)
            button.setEnabled(False)
            button.clicked.connect(callback)
            setattr(self, attr_name, button)
            self.add_widget(button)
        
    def add_widget(self, widget):
        """Add widget to the layout."""
        self._layout.addWidget(widget)
        
    def add_layout(self, layout):
        """Add layout to the main layout."""
        self._layout.addLayout(layout)

    def _set_widget_status(self, enable: bool) -> None:
        """Set all widget's buttons enable/disable"""
        for bttn, _, _ in self.buttons_config:
            getattr(bttn).setEnabled(enable)

    def _disable_widget(self, event: Event) -> None:
        self._set_widget_status(False)

    def _unable_widget(self, event: Event) -> None:
        self._set_widget_status(True)