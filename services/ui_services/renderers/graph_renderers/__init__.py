from .hist_renderer import HistRenderer
from .edf_renderer import EDFRenderer
from .dist_renderer import DistributionRenderer

from .graph2var_renderers.corr_field_renderer import CorrelationFieldRenderer
from .graph2var_renderers.hist3D_renderer import Histogram3DRenderer

RENDERERS = {
    'histogram': HistRenderer,
    'edf': EDFRenderer,
    'distribution': DistributionRenderer,

    'correlation_field': CorrelationFieldRenderer,
    'histogram3D': Histogram3DRenderer
}