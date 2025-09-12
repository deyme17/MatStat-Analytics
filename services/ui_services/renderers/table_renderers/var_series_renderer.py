from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


class VarSerRenderer:
    """Handles rendering of variation series data into a QTableWidget with consistent formatting."""

    def __init__(self, table: QTableWidget):
        self._table = table