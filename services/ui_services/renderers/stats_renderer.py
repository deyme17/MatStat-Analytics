from typing import Dict, Tuple
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

class TableRenderer:
    """Handles rendering of statistical data into Qt tables with consistent formatting."""

    CI_MAPPING = {
        'Mean': 'Mean CI',
        'RMS deviation': 'Std Deviation CI',
        'Variance': 'Variance CI',
        'MED': 'MED CI',
        'Assymetry coeff.': 'Assymetry coeff. CI',
        'Excess': 'Excess CI'
    }

    @classmethod
    def render_stats_table(
        cls,
        table: QTableWidget,
        stats_data: Dict[str, float],
        ci_data: Dict[str, Tuple[float, float]],
        precision: int = 2
    ) -> None:
        """
        Renders statistics with confidence intervals into a table.
        
        Args:
            table: Target QTableWidget
            stats_data: Basic statistics {metric: value}
            ci_data: Confidence intervals {metric: (lower, upper)}
            precision: Rounding precision
        """
        cls._setup_table_headers(table)
        cls._populate_table_data(table, stats_data, ci_data, precision)

    @staticmethod
    def _setup_table_headers(table: QTableWidget) -> None:
        """Configures table structure and headers."""
        table.clearContents()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
        table.setRowCount(0)

    @classmethod
    def _populate_table_data(
        cls,
        table: QTableWidget,
        stats_data: Dict[str, float],
        ci_data: Dict[str, Tuple[float, float]],
        precision: int
    ) -> None:
        """Fills table with statistical data."""
        table.setRowCount(len(stats_data))
        
        for row, (metric, value) in enumerate(stats_data.items()):
            table.setVerticalHeaderItem(row, QTableWidgetItem(metric))
            
            # Format main value
            table.setItem(row, 1, QTableWidgetItem(f"{value:.{precision}f}"))
            
            # Format CI values
            ci_metric = cls.CI_MAPPING.get(metric)
            lower, upper = ci_data.get(ci_metric, ("N/A", "N/A"))
            
            table.setItem(row, 0, QTableWidgetItem(
                f"{lower:.{precision}f}" if isinstance(lower, (int, float)) else str(lower)
            ))
            table.setItem(row, 2, QTableWidgetItem(
                f"{upper:.{precision}f}" if isinstance(upper, (int, float)) else str(upper)
            ))