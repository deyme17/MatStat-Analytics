from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QHeaderView

class StatisticTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self._init_confidence_table()

    def _init_confidence_table(self):
        self.conf_label = QLabel("Confidence Intervals Table")
        self.conf_table = QTableWidget()
        self.conf_table.setColumnCount(3)
        self.conf_table.setHorizontalHeaderLabels(['Lower CI', 'Value', 'Upper CI'])
        self.conf_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.layout.addWidget(self.conf_label)
        self.layout.addWidget(self.conf_table)

    def update_confidence_table(self, data: list[tuple]):
        """
        Update the Table of confidence intervals.
        Data - List of Tuples (Lower, Value, Upper)
        """
        self.conf_table.setRowCount(len(data))
        for i, (lower, val, upper) in enumerate(data):
            self.conf_table.setItem(i, 0, self._item(lower))
            self.conf_table.setItem(i, 1, self._item(val))
            self.conf_table.setItem(i, 2, self._item(upper))

    def _item(self, val):
        from PyQt6.QtWidgets import QTableWidgetItem
        return QTableWidgetItem(f"{val:.4f}")
