from .univariate.hist_renderer import HistRenderer
from .univariate.edf_renderer import EDFRenderer
from .univariate.dist_renderer import DistributionRenderer
from .univariate.hh_renderer import HHRenderer

from .bivariate.corr_field_renderer import CorrelationFieldRenderer
from .bivariate.histMap_renderer import HistogramMapRenderer
from .trivariate.bubble_plot_renderer import BubblePlotRenderer

from .multivariate.corr_matrix_renderer import CorrMatrixRenderer
from .multivariate.scatter_matrix_renderer import ScatterMatrixRenderer
from .multivariate.heatmap_renderer import HeatMapRenderer
from .multivariate.parallel_coord_renderer import ParallelCoordsRenderer

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