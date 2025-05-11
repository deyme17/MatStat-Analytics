from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from utils.ui_styles import groupStyle, groupMargin

class BaseTestPanel(QGroupBox):
    def __init__(self, title, window):
        super().__init__(title)
        self.window = window
        self.setCheckable(False)
        self.setStyleSheet(groupStyle + groupMargin)

        self.hypothesis_result = QLabel("[ ] Hypothesis H₀ not tested")
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

    def add_stat_label(self, prefix: str = " "):
        label = QLabel(prefix)
        self._layout.addWidget(label)
        return label

    def finalize_layout(self, *extra_widgets):
        for w in extra_widgets:
            self._layout.addWidget(w)
        self._layout.addWidget(self.hypothesis_result)

    def update_result(self, passed: bool):
        self.hypothesis_result.setText(
            f"[{'✓' if passed else '✗'}] Hypothesis H₀ {'not rejected' if passed else 'rejected'}"
        )

    def evaluate(self, data, dist, alpha):
        raise NotImplementedError("Subclasses must implement evaluate()")
    
    def clear(self):
        self.hypothesis_result.setText("[ ] Hypothesis H₀ not tested")

