from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from views.widgets.homogenwidgets.panels.homogen_panel import BaseHomoTestPanel
from views.widgets.utils import make_button


class HomoTestSectionGroup(QGroupBox):
    """Section container grouping a list of homogeneity test panels with run/clear actions."""
    def __init__(self, title: str, panels: list[BaseHomoTestPanel], on_run: callable, parent=None) -> None:
        super().__init__(title, parent)
        self.panels = panels
        self.on_run = on_run
        self._init_ui()

    def _init_ui(self) -> None:
        """Build test section layout."""
        layout = QVBoxLayout(self)

        self.combo = QComboBox()
        for panel in self.panels:
            self.combo.addItem(panel.get_test_name() or "Unknown")

        layout.addWidget(QLabel("Select test:"))
        layout.addWidget(self.combo)

        btns_layout = QHBoxLayout()
        run_btn = make_button("Run test")
        clear_btn = make_button("Clear")
        btns_layout.addWidget(run_btn)
        btns_layout.addWidget(clear_btn)
        layout.addLayout(btns_layout)

        for panel in self.panels:
            panel.hide()
            layout.addWidget(panel)

        clear_btn.clicked.connect(self._clear_panels)
        run_btn.clicked.connect(lambda: self.on_run(self))

    def _clear_panels(self) -> None:
        """Clear and hide all panels within section."""
        for panel in self.panels:
            panel.clear()
            panel.hide()

    def get_selected_panel(self) -> BaseHomoTestPanel | None:
        """Return currently selected test panel."""
        idx = self.combo.currentIndex()
        if 0 <= idx < len(self.panels):
            return self.panels[idx]
        return None