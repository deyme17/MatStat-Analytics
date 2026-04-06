from PyQt6.QtWidgets import QComboBox, QLabel, QHBoxLayout, QWidget
from ..graph_tab import BaseGraphTab
from typing import Tuple, Optional, List
from utils import AppContext, EventBus, EventType, Event

CONTROLS_HEIGHT = 25
CONTROLS_WIDTH = 300


class Base3VarGraphTab(BaseGraphTab):
    """Base class for graph tabs that work with three variables"""    
    def __init__(self, name: str, context: AppContext):
        super().__init__(name=name, context=context)
        self.event_bus: EventBus = context.event_bus
        
        self.second_column_selector: QComboBox = None
        self.third_column_selector: QComboBox = None
        
        self._add_column_selectors()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        """Subscribe to data change events"""
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED, self._on_dataset_changed)
        self.event_bus.subscribe(EventType.DATASET_CHANGED, self._on_dataset_changed)
        self.event_bus.subscribe(EventType.COLUMN_CHANGED, self._on_dataset_changed)

    def _on_dataset_changed(self, event: Event) -> None:
        self.update_column_list()
        if self.get_current_column_names():
            self.draw()
    
    def _add_column_selectors(self) -> None:
        """Add column selectors at the bottom with fixed height & width"""
        self.selector_widget = QWidget()
        self.selector_widget.setFixedHeight(CONTROLS_HEIGHT)
        self.selector_widget.setFixedWidth(CONTROLS_WIDTH)

        selector_layout = QHBoxLayout()
        selector_layout.setContentsMargins(5, 2, 5, 2)
        
        # second column
        label1 = QLabel("Second column:")
        self.second_column_selector = QComboBox()
        self.second_column_selector.currentTextChanged.connect(self.draw)
        selector_layout.addWidget(label1)
        selector_layout.addWidget(self.second_column_selector, stretch=1)

        # third column
        label2 = QLabel("Third column:")
        self.third_column_selector = QComboBox()
        self.third_column_selector.currentTextChanged.connect(self.draw)
        selector_layout.addWidget(label2)
        selector_layout.addWidget(self.third_column_selector, stretch=1)

        self.selector_widget.setLayout(selector_layout)

        # add at the very bottom after canvas
        main_layout = self.layout()
        main_layout.addWidget(self.selector_widget)

    def update_column_list(self, columns: List[str] = None) -> None:
        """Update available columns in selectors from data model or provided list"""
        if columns is None:
            data_model = self.get_data_model()
            if data_model is None or data_model.dataframe is None:
                self.second_column_selector.clear()
                self.third_column_selector.clear()
                return
            columns = list(data_model.dataframe.columns)
        
        if len(columns) < 3:
            self.second_column_selector.clear()
            self.third_column_selector.clear()
            self.clear()
            return
        
        first_col = self.context.version_manager.get_current_column_name()
        current1 = self.second_column_selector.currentText().strip()
        current2 = self.third_column_selector.currentText().strip()

        # define available options for selectors
        columns1 = [col for col in columns if col != first_col]
        columns2 = [col for col in columns if col != first_col]
        if current1:
            columns2 = [col for col in columns2 if col != current1]
        if current2:
            columns1 = [col for col in columns1 if col != current2]

        # update second selector
        self.second_column_selector.blockSignals(True)
        self.second_column_selector.clear()
        self.second_column_selector.addItems(columns1)
        if current1 and current1 in columns1:
            self.second_column_selector.setCurrentText(current1)
        else:
            self.second_column_selector.setCurrentIndex(0)  # default
        self.second_column_selector.blockSignals(False)

        # update third selector
        self.third_column_selector.blockSignals(True)
        self.third_column_selector.clear()
        self.third_column_selector.addItems(columns2)
        if current2 and current2 in columns2:
            self.third_column_selector.setCurrentText(current2)
        else:
            self.third_column_selector.setCurrentIndex(1)  # default
        self.third_column_selector.blockSignals(False)

    def get_current_column_names(self) -> Optional[Tuple[str, str, str]]:
        """Returns the names of the three chosen columns"""
        data_model = self.get_data_model()
        if data_model is None or data_model.dataframe is None:
            return None
        
        available_columns = list(data_model.dataframe.columns)
        first_col = self.context.version_manager.get_current_column_name()
        second_col = self.second_column_selector.currentText()
        third_col = self.third_column_selector.currentText()

        # validate selections
        if not first_col or not second_col or not third_col:
            return None
        if len({first_col, second_col, third_col}) < 3:
            return None
        if first_col not in available_columns or second_col not in available_columns or third_col not in available_columns:
            return None
        
        return first_col, second_col, third_col