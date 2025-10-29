from PyQt6.QtWidgets import QComboBox, QLabel, QHBoxLayout, QWidget
from ..graph_tab import BaseGraphTab
from typing import Tuple, Optional, List
from utils import AppContext, EventBus, EventType

CONTROLS_HEIGHT = 25
CONTROLS_WIDTH = 300


class Base2VarGraphTab(BaseGraphTab):
    """Base class for graph tabs that work with two variables"""
    def __init__(self, name: str, context: AppContext):
        """
        Args:
            name: Tab name
            context: Application context
        """
        super().__init__(name=name, context=context)
        self.event_bus: EventBus = context.event_bus
        self.second_column_selector = None
        self._add_column_selector()

    def _subscribe_to_events(self) -> None:
        """Subscribe to data change events"""
        self.event_bus.subscribe(EventType.DATA_LOADED, self.update_column_list)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self.update_column_list)
    
    def _add_column_selector(self) -> None:
        """Add second column selector at the very bottom with fixed height & width"""
        # selector widget with fixed height
        self.selector_widget = QWidget()
        self.selector_widget.setFixedHeight(CONTROLS_HEIGHT)
        self.selector_widget.setFixedWidth(CONTROLS_WIDTH)
        selector_layout = QHBoxLayout()
        selector_layout.setContentsMargins(5, 2, 5, 2)
        
        label = QLabel("Second column:")
        self.second_column_selector = QComboBox()
        self.second_column_selector.currentTextChanged.connect(self.draw)
        
        selector_layout.addWidget(label)
        selector_layout.addWidget(self.second_column_selector, stretch=1)
        self.selector_widget.setLayout(selector_layout)
        
        # add at the very bottom after canvas
        main_layout = self.layout()
        main_layout.addWidget(self.selector_widget)
    
    def update_column_list(self, columns: List[str] = None) -> None:
        """Update available columns in selector from data model or provided list"""
        # if columns not provided, get from data model
        if columns is None:
            data_model = self.get_data_model()
            if data_model is None or data_model.dataframe is None:
                self.second_column_selector.clear()
                return
            columns = list(data_model.dataframe.columns)
        
        current = self.second_column_selector.currentText()
        self.second_column_selector.blockSignals(True)
        self.second_column_selector.clear()
        self.second_column_selector.addItems(columns)
        
        if current in columns:
            self.second_column_selector.setCurrentText(current)
        elif columns:
            # select first column if current is not available
            self.second_column_selector.setCurrentIndex(0)
        
        self.second_column_selector.blockSignals(False)
    
    def get_current_column_names(self) -> Optional[Tuple[str, str]]:
        """
        Returnes the names of two choosen columns
        """
        data_model = self.get_data_model()
        if data_model is None or data_model.dataframe is None:
            return
        
        first_col = self.context.version_manager.get_current_column_name()
        second_col = self.second_column_selector.currentText()
        
        return first_col, second_col