from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QHeaderView
)

class StatisticTab(QWidget):
    """
    A QWidget tab displaying a table of confidence intervals
    for statistical summaries and variation series.
    """
    def __init__(self, stat_renderer_cls, var_rendere_cls, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.conf_label = QLabel("Confidence Intervals Table")
        self.conf_table = QTableWidget()
        self.conf_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.conf_label)
        self.layout.addWidget(self.conf_table)
        self.stat_renderer = stat_renderer_cls(self.conf_table)

        self.var_label = QLabel("Variation Series Table")
        self.var_table = QTableWidget()
        self.var_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.layout.addWidget(self.var_label)
        self.layout.addWidget(self.var_label)
        self.var_renderer = var_rendere_cls(self.var_table)