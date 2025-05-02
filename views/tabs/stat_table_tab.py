from PyQt6.QtWidgets import QTableWidget, QHeaderView

def create_statistic_tab():
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    return table