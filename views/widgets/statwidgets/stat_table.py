from PyQt6.QtWidgets import QTableWidget, QHeaderView

def create_stat_table():
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    return table
