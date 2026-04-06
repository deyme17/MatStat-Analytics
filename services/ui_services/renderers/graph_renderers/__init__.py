from .hist_renderer import HistRenderer
from .edf_renderer import EDFRenderer
from .dist_renderer import DistributionRenderer
from .hh_renderer import HHRenderer

from .reg_plot_dialog_renderer import RegressionPlotDialog
from .resfitted_plot_renderer import ResidualsFittedPlot

from .graph2var_renderers.corr_field_renderer import CorrelationFieldRenderer
from .graph2var_renderers.histMap_renderer import HistogramMapRenderer
from .graph3var_renderers.bubble_plot_renderer import BubblePlotRenderer

from .graphMultivar_renderers.corr_matrix_renderer import CorrMatrixRenderer
from .graphMultivar_renderers.heatmap_renderer import HeatMapRenderer
from .graphMultivar_renderers.parallel_coord_renderer import ParallelCoordsRenderer

from .graph_renderer import Renderer

RENDERERS: dict[str, type[Renderer]] = {
    'histogram': HistRenderer,
    'edf': EDFRenderer,
    'distribution': DistributionRenderer,
    'hh_plot': HHRenderer,

    'correlation_field': CorrelationFieldRenderer,
    'histogram_map': HistogramMapRenderer,
    'bubble_plot': BubblePlotRenderer,
    
    'correlation_matrix': CorrMatrixRenderer,
    'heatmap': HeatMapRenderer,
    'parallel_coordinates': ParallelCoordsRenderer,
}