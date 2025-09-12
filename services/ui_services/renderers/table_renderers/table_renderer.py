from PyQt6.QtWidgets import QTableWidget
from abc import ABC, abstractmethod


class TableRenderer(ABC):
    def __init__(self, table: QTableWidget):
        self._table = table

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def _setup_headers(self) -> None:
        pass
    
    @abstractmethod
    def _populate() -> None:
        pass