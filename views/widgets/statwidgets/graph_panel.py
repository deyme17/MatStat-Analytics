from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QDoubleSpinBox, QCheckBox, QTabWidget
)
from views.widgets.statwidgets.graph_tabs import registered_graphs
import pandas as pd


class GraphPanel(QWidget):
    """
    Main UI panel that hosts graph tabs and user controls for visualization.
    Delegates all logic to the GraphController.
    """

    def __init__(self, window, dist_selector, graph_controller=None):
        """
        Initialize the graph panel and controls.

        :param window: main application window
        :param graph_controller: GraphController instance to handle logic
        :param dist_selector: class (not instance) for distribution selector
        """
        super().__init__(window)
        self.window = window
        self.graph_controller = graph_controller                                                    # TODO
        self.data = None
        self.graph_tabs = {}

        self._init_controls(dist_selector)
        self._connect_controls()

        self.tabs = QTabWidget()
        for name, tab_cls in registered_graphs.items():
            tab = tab_cls()
            tab.set_context(self)
            self.tabs.addTab(tab, name)
            self.graph_tabs[name] = tab

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addLayout(self.controls_layout)
        layout.addWidget(self.dist_selector)
        self.setLayout(layout)

    def _init_controls(self, dist_selector_cls):
        """Initialize spinboxes, checkboxes, and selector UI."""
        self.controls_layout = QHBoxLayout()

        self.bins_spinbox = QSpinBox()
        self.bins_spinbox.setRange(1, 999)
        self.bins_spinbox.setValue(10)
        self.bins_spinbox.setMaximumWidth(100)

        self.confidence_spinbox = QDoubleSpinBox()
        self.confidence_spinbox.setRange(0.80, 0.99)
        self.confidence_spinbox.setSingleStep(0.01)
        self.confidence_spinbox.setValue(0.95)
        self.confidence_spinbox.setDecimals(2)

        self.show_kde_checkbox = QCheckBox("Show KDE")
        self.show_kde_checkbox.setChecked(False)

        self.controls_layout.addWidget(QLabel("Bins:"))
        self.controls_layout.addWidget(self.bins_spinbox)
        self.controls_layout.addSpacing(20)
        self.controls_layout.addWidget(QLabel("Confidence:"))
        self.controls_layout.addWidget(self.confidence_spinbox)
        self.controls_layout.addStretch()
        self.controls_layout.addWidget(self.show_kde_checkbox)

        self.dist_selector = dist_selector_cls()

    def _connect_controls(self):
        """Connect user controls to controller callbacks."""
        self.bins_spinbox.valueChanged.connect(self.window.graph_controller.on_bins_changed)         # TODO  
        self.confidence_spinbox.valueChanged.connect(self.window.graph_controller.on_alpha_changed)  # TODO
        self.show_kde_checkbox.stateChanged.connect(self.window.graph_controller.on_kde_toggled)     # TODO
        self.dist_selector.set_on_change(self.window.graph_controller.on_distribution_changed)       # TODO

    def set_data(self, data: pd.Series):
        """
        Set new data to be visualized.

        :param data: input data series
        """
        self.data = data
        if data is not None:
            self.bins_spinbox.setMaximum(len(data))
        self.graph_controller.plot_all()

    def refresh_all(self):
        """
        Redraw all graph tabs using current clean data.
        """
        if self.data is None or self.data.empty:
            return

        clean_data = self.data.dropna()
        if clean_data.empty:
            return

        for tab in self.graph_tabs.values():
            tab.draw(clean_data)

    def clear(self):
        """Clear all graph tabs."""
        for tab in self.graph_tabs.values():
            tab.clear()

    def get_selected_distribution(self):
        """Return selected distribution object or None."""
        return self.dist_selector.get_selected_distribution()

    def get_render_params(self):
        """
        Get current rendering parameters from the UI.

        :return: dictionary with 'bins', 'kde', 'confidence', and 'distribution'
        """
        return {
            "bins": self.bins_spinbox.value(),
            "kde": self.show_kde_checkbox.isChecked(),
            "confidence": self.confidence_spinbox.value(),
            "distribution": self.get_selected_distribution()
        }
