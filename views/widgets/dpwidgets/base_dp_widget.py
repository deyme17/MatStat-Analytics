from PyQt6.QtWidgets import QGroupBox, QVBoxLayout
from types import SimpleNamespace
from utils.ui_styles import groupStyle

class BaseDataWidget(QGroupBox):
    """Base class for all data processing widgets."""
    def __init__(self, title, controller):
        super().__init__(title)
        self.controller = controller
        self.attr = SimpleNamespace()
        self.setStyleSheet(groupStyle)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
    def add_widget(self, widget):
        """Add widget to the layout."""
        self.layout.addWidget(widget)
        
    def add_layout(self, layout):
        """Add layout to the main layout."""
        self.layout.addLayout(layout)