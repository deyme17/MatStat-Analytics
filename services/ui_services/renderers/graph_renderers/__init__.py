from .graph1var_renderers.hist_renderer import HistRenderer
from .graph1var_renderers.edf_renderer import EDFRenderer
from .graph1var_renderers.dist_renderer import DistributionRenderer
from .graph1var_renderers.hh_renderer import HHRenderer

from .graph2var_renderers.corr_field_renderer import CorrelationFieldRenderer
from .graph2var_renderers.histMap_renderer import HistogramMapRenderer
from .graph3var_renderers.bubble_plot_renderer import BubblePlotRenderer

from .graphMultivar_renderers.corr_matrix_renderer import CorrMatrixRenderer
from .graphMultivar_renderers.scatter_matrix_renderer import ScatterMatrixRenderer
from .graphMultivar_renderers.heatmap_renderer import HeatMapRenderer
from .graphMultivar_renderers.parallel_coord_renderer import ParallelCoordsRenderer

from .reg_plot_dialog_renderer import RegressionPlotDialog
from .resfitted_plot_renderer import ResidualsFittedPlot

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
    'scatter_matrix': ScatterMatrixRenderer,
    'heatmap': HeatMapRenderer,
    'parallel_coordinates': ParallelCoordsRenderer,
}