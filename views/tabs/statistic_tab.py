from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QHeaderView
)
from services.ui_services.renderers.table_renderers.table_renderer import TableRenderer



class StatisticTab(QWidget):
    """
    A QWidget tab displaying a table of confidence intervals
    for statistical summaries and variation series.
    """
    def __init__(self, stat_renderer_cls: type[TableRenderer], 
                       var_renderer_cls: type[TableRenderer],
                       multi_renderer_cls: type[TableRenderer],    
                       parent=None):
        """
        Args:
            stat_renderer_cls: Class for rendering statistic table.
            var_renderer_cls: Class for rendering variation series.
            multi_renderer_cls: Class for rendering multivariate table.
            parent: Parent widget.
        """
        super().__init__(parent)
        self._layout = QVBoxLayout(self)

        self.conf_label = QLabel("Confidence Intervals Table")
        self.conf_table = QTableWidget()
        self.conf_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._layout.addWidget(self.conf_label)
        self._layout.addWidget(self.conf_table)
        self.stat_renderer = stat_renderer_cls(self.conf_table)

        self.var_label = QLabel("Variation Series Table")
        self.var_table = QTableWidget()
        self.var_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._layout.addWidget(self.var_label)
        self._layout.addWidget(self.var_table)
        self.var_renderer = var_renderer_cls(self.var_table)

        self.multi_label = QLabel("Multivariable Table")
        self.multi_table = QTableWidget()
        self.multi_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._layout.addWidget(self.multi_label)
        self._layout.addWidget(self.multi_table)
        self.multi_renderer = multi_renderer_cls(self.multi_table)