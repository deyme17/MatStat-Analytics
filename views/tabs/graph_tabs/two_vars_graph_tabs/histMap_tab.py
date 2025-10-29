from PyQt6.QtWidgets import QSpinBox, QLabel
from .base_2varGraph_tab import Base2VarGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS
from utils import AppContext

DEFAULT_BINS = 10
MIN_BINS = 2
MAX_BINS = 100


class HistogramMapTab(Base2VarGraphTab):
    """Tab for 3D histogram map visualization"""
    def __init__(self, context: AppContext):
        super().__init__(name="3D Histogram Map", context=context)
        self._add_bins_control()
    
    def _add_bins_control(self):
        """Add bins control to the second column selector row"""
        # get the selector widget from parent (last widget in layout)
        main_layout = self.layout()
        selector_widget = main_layout.itemAt(main_layout.count() - 1).widget()
        selector_layout = selector_widget.layout()
        
        # add bins control to the same row
        label_bins = QLabel("Bins:")
        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(MIN_BINS, MAX_BINS)
        self.bins_spinbox.setValue(DEFAULT_BINS)
        self.bins_spinbox.setMaximumWidth(80)
        self.bins_spinbox.valueChanged.connect(self._on_bins_changed)
        
        selector_layout.addSpacing(20)
        selector_layout.addWidget(label_bins)
        selector_layout.addWidget(self.bins_spinbox)
    
    def _on_bins_changed(self):
        """Handle bins value change"""
        if self.panel:
            self.draw()
    
    def draw(self):
        """Draw 3D histogram as heatmap for two columns"""
        self.clear()
        try:
            data_model = self.get_data_model()
            col1, col2 = self.get_current_column_names()
            renderer = RENDERERS['histogram_map']
            renderer.render(
                self.ax, 
                data_model.dataframe,
                col1,
                col2,
                bins1=data_model.bins,
                bins2=self.bins_spinbox.value()
            )
            self.apply_default_style(self.ax, col1, col2)
            self.canvas.draw()
        except Exception as e:
            print(f"Histogram Map Error: {e}")
            self.clear()