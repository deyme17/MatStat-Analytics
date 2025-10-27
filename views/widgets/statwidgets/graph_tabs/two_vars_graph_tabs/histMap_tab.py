from .base_2varGraph_tab import Base2VarGraphTab
from services.ui_services.renderers.graph_renderers import RENDERERS
import matplotlib.pyplot as plt
from utils import AppContext


class HistogramMapTab(Base2VarGraphTab):
    """Tab for 3D histogram map visualization"""
    def __init__(self, context: AppContext):
        super().__init__(name="3D Histogram Map", context=context)