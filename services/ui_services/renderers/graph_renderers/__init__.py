from .hist_renderer import HistRenderer
from .edf_renderer import EDFRenderer
from .dist_renderer import DistributionRenderer
from .hh_renderer import HHRenderer
from .corr_matrix_renderer import CorrMatrixRenderer

from .graph2var_renderers.corr_field_renderer import CorrelationFieldRenderer
from .graph2var_renderers.histMap_renderer import HistogramMapRenderer

from .graph_renderer import Renderer

RENDERERS: dict[str, type[Renderer]] = {
    'histogram': HistRenderer,
    'edf': EDFRenderer,
    'distribution': DistributionRenderer,
    'hh_plot': HHRenderer,
    'correlation_matrix': CorrMatrixRenderer,

    'correlation_field': CorrelationFieldRenderer,
    'histogram_map': HistogramMapRenderer
}