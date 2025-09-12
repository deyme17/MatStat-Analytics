from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from .table_renderer import TableRenderer


class StatsRenderer(TableRenderer):
    """Handles rendering of statistical data into a QTableWidget with consistent formatting."""

    CI_MAPPING = {
        'Mean': 'Mean CI',
        'RMS deviation': 'Std Deviation CI',
        'Variance': 'Variance CI',
        'MED': 'MED CI',
        'Assymetry coeff.': 'Assymetry coeff. CI',
        'Excess': 'Excess CI'
    }

    def __init__(self, table: QTableWidget):
        super().__init__(table)

    def render(self, stats_data: dict[str, float], ci_data: dict[str, tuple], precision: int = 2) -> None:
        """Renders statistics with confidence intervals into the attached table."""
        self._setup_headers()
        self._populate(stats_data, ci_data, precision)

    def _setup_headers(self) -> None:
        self._table.clearContents()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
        self._table.setRowCount(0)

    def _populate(self, stats_data: dict[str, float], ci_data: dict[str, tuple], precision: int) -> None:
        self._table.setRowCount(len(stats_data))

        for row, (metric, value) in enumerate(stats_data.items()):
            self._table.setVerticalHeaderItem(row, QTableWidgetItem(metric))

            # main value
            self._table.setItem(row, 1, QTableWidgetItem(f"{value:.{precision}f}"))

            # confidence interval
            ci_metric = self.CI_MAPPING.get(metric)
            lower, upper = ci_data.get(ci_metric, ("N/A", "N/A"))

            self._table.setItem(
                row, 0,
                QTableWidgetItem(f"{lower:.{precision}f}" if isinstance(lower, (int, float)) else str(lower))
            )
            self._table.setItem(
                row, 2,
                QTableWidgetItem(f"{upper:.{precision}f}" if isinstance(upper, (int, float)) else str(upper))
            )