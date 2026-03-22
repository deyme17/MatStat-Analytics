from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from .table_renderer import TableRenderer


class MultiVarRenderer(TableRenderer):
    """Renders statistical data into a QTableWidget where columns are variables and rows are statistics."""
    def __init__(self, table: QTableWidget):
        super().__init__(table)

    def render(self, data: dict[str, dict[str, float]], precision: int = 2) -> None:
        """
        Renders a multi-variable statistics table.

        Args:
            data: {variable_name: {stat_name: value, ...}, ...}
            precision: number of decimal places for float values
        """
        if not data:
            self._table.clearContents()
            self._table.setRowCount(0)
            self._table.setColumnCount(0)
            return

        variables = list(data.keys())
        stats = list(next(iter(data.values())).keys())

        self._setup_headers(variables, stats)
        self._populate(data, variables, stats, precision)

    def _setup_headers(self, variables: list[str] = None, stats: list[str] = None) -> None:
        self._table.clearContents()
        self._table.setColumnCount(len(variables) if variables else 0)
        self._table.setRowCount(len(stats) if stats else 0)
        if variables:
            self._table.setHorizontalHeaderLabels(variables)
        if stats:
            self._table.setVerticalHeaderLabels(stats)

    def _populate(
        self,
        data: dict[str, dict[str, float]],
        variables: list[str],
        stats: list[str],
        precision: int,
    ) -> None:
        for col, variable in enumerate(variables):
            var_stats = data[variable]
            for row, stat in enumerate(stats):
                value = var_stats.get(stat)
                if value is None:
                    text = "N/A"
                elif isinstance(value, (int, float)):
                    text = f"{value:.{precision}f}"
                else:
                    text = str(value)
                self._table.setItem(row, col, QTableWidgetItem(text))