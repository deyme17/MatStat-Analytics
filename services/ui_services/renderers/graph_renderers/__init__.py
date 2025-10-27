from .hist_renderer import HistRenderer
from .edf_renderer import EDFRenderer
from .dist_renderer import DistributionRenderer

from .graph2var_renderers.corr_field_renderer import CorrelationFieldRenderer
from .graph2var_renderers.histMap_renderer import HistogramMapRenderer

RENDERERS = {
    'histogram': HistRenderer,
    'edf': EDFRenderer,
    'distribution': DistributionRenderer,

    'correlation_field': CorrelationFieldRenderer,
    'histogramMao': HistogramMapRenderer
}