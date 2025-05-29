from PyQt6.QtWidgets import QTableWidget, QHeaderView

def create_stat_table():
    """
    Creates a QTableWidget for displaying statistical characteristics 
    along with their confidence intervals.

    Returns:
        QTableWidget: A table with 3 columns — Lower CI, Value, Upper CI —
        and stretchable horizontal headers.
    """
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    return table
