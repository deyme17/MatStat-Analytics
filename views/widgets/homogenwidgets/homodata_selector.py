from PyQt6.QtWidgets import QCheckBox
from views.widgets.utils.common_widgets import FeatureSelectorWidget

MAX_GROUP_HEIGHT = 159
LIST_WIDGET_HEIGHT = 150
LIST_WIDGET_WIDTH = 320


class HomoDataSelectorWidget(FeatureSelectorWidget):
    """Dataset selection group widget with sample independence configuration."""
    def __init__(self, parent=None) -> None:
        super().__init__(
            title="Select datasets for testing",
            label_prefix="datasets",
            height=LIST_WIDGET_HEIGHT,
            width=LIST_WIDGET_WIDTH,
            parent=parent
        )
        self._init_extra_controls()

    def _init_extra_controls(self) -> None:
        """Add independence checkbox to layout."""
        self.independence_checkbox = QCheckBox("Samples are independent")
        self.independence_checkbox.setChecked(False)
        self.layout().addWidget(self.independence_checkbox)
        self.setMaximumHeight(MAX_GROUP_HEIGHT)

    def is_independent(self) -> bool:
        """Return status of independence checkbox."""
        return self.independence_checkbox.isChecked()