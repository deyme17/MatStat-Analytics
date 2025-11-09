from PyQt6.QtWidgets import QCheckBox
from .base_2varGraph_tab import Base2VarGraphTab
from services import SimpleLinearRegression
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext
import pandas as pd


class CorrelationFieldTab(Base2VarGraphTab):
    """Tab for correlation field visualization"""
    def __init__(self, context: AppContext, slr: SimpleLinearRegression):
        super().__init__(name="Correlation Field", context=context)
        self._add_regression_line_checkbox()
        self.slr: SimpleLinearRegression = slr

    def _add_regression_line_checkbox(self):
        """Add regression line checkbox to the second column selector row"""
        # get the selector widget from parent (last widget in layout)
        main_layout = self.layout()
        selector_widget = main_layout.itemAt(main_layout.count() - 1).widget()
        selector_layout = selector_widget.layout()
        
        # add regression line checkbox to the same row
        self.regression_checkbox = QCheckBox("Regression line")
        self.regression_checkbox.setChecked(False)
        self.regression_checkbox.stateChanged.connect(self._on_regression_line_toggled)
        
        selector_layout.addSpacing(20)
        selector_layout.addWidget(self.regression_checkbox)
    
    def _on_regression_line_toggled(self):
        """Handle regression line checkbox changing"""
        if self.panel:
            self.draw()

    def draw(self):
        """Draw correlation field for two columns"""
        self.clear()
        try:
            data_model = self.get_data_model()
            if data_model is None or data_model.dataframe is None or data_model.dataframe.empty:
                return
            columns = self.get_current_column_names()
            if columns is None:
                return
            col1, col2 = columns
            if not col1 or not col2:
                return
            
            # regression line
            regression_coeffs = None
            if self.regression_checkbox.isChecked():
                regression_coeffs = self.slr.calculate_regression_coeffs(data_model.dataframe[col1], data_model.dataframe[col2])
            
            renderer = RENDERERS['correlation_field']
            renderer.render(self.ax, data_model.dataframe, col1, col2, regression_coeffs)
            self.apply_default_style(self.ax, col1, col2)
            self.canvas.draw()
        except Exception as e:
            print(f"Correlation Field Error: {e}")
            self.clear()