from .hist_tab import HistogramTab
from .edf_tab import EDFTab

registered_graphs = {
    "Histogram": HistogramTab,
    "Empirical Distribution Function": EDFTab
}