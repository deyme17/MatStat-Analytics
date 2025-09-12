from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from .table_renderer import TableRenderer


class VarSerRenderer(TableRenderer):
    """Handles rendering of variation series data into a QTableWidget with consistent formatting."""

    def __init__(self, table: QTableWidget):
        super().__init__(table)

    def render(self, data: dict[str, float]) -> None:
        ...

    def _setup_headers(self) -> None:
        ...

    def _populate(self, stats_data: dict[str, float], ci_data: dict[str, tuple], precision: int) -> None:
        ...

        for row, (metric, value) in enumerate(stats_data.items()):
            ...