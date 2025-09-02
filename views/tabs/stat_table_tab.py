from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QHeaderView
)

class StatisticTab(QWidget):
    """
    A QWidget tab displaying a table of confidence intervals
    for statistical summaries.
    """
    def __init__(self, renderer_cls, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.conf_label = QLabel("Confidence Intervals Table")
        self.conf_table = QTableWidget()
        self.conf_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.layout.addWidget(self.conf_label)
        self.layout.addWidget(self.conf_table)

        self.renderer = renderer_cls(self.conf_table)