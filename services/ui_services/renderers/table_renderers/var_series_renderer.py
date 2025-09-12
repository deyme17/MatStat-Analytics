from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from .table_renderer import TableRenderer


class VarSerRenderer(TableRenderer):
    """Handles rendering of variation series data into a QTableWidget with consistent formatting."""

    def __init__(self, table: QTableWidget):
        super().__init__(table)

    def render(self, series_data: dict) -> None:
        """Renders variation series into the attached table."""
        self._setup_headers()
        self._populate(series_data)

    def _setup_headers(self) -> None:
        self._table.clearContents()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(['Boundaries', 'Midpoints', 'Frequency', 'Relative Freq.', 'Cumulative Rel.Freq.'])
        self._table.setRowCount(0)

    def _populate(self, data: dict) -> None:
        if not data:
            return
        
        row_count = len(next(iter(data.values())))
        self._table.setRowCount(row_count)
        
        for row in range(row_count):
            self._table.setVerticalHeaderItem(row, QTableWidgetItem(str(data['N'][row])))
            self._table.setItem(row, 0, QTableWidgetItem(str(data['Boundaries'][row])))
            self._table.setItem(row, 1, QTableWidgetItem(f"{data['Midpoints'][row]:.2f}"))
            self._table.setItem(row, 2, QTableWidgetItem(str(data['Frequency'][row])))
            self._table.setItem(row, 3, QTableWidgetItem(f"{data['Relative Freq.'][row]:.4f}"))
            self._table.setItem(row, 4, QTableWidgetItem(f"{data['Cumulative Rel.Freq.'][row]:.4f}"))