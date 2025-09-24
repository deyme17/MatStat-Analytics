from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from abc import ABC, abstractmethod
import pandas as pd
from utils.ui_styles import groupStyle, groupMargin


class Meta(type(QGroupBox), type(ABC)):
    pass


class BaseHomoTestPanel(QGroupBox, ABC, metaclass=Meta):
    """
    Abstract base class for homogeneity test panels.
    Accepts a dynamic list of statistics for flexible test panels.
    """
    def __init__(self, homogen_controller, stats_config: list[dict]) -> None:
        """
        Initialize the panel with given stats configuration.
        Args:
            homogen_controller: Controller for executing tests.
            stats_config (list[dict]): List of dictionaries with keys:
                - "key": str, result dict key
                - "label": str, label prefix
        """
        super().__init__()
        self.homogen_controller = homogen_controller
        self.setCheckable(False)
        self.setStyleSheet(groupStyle + groupMargin)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # dict for storing QLabel references
        self.stat_labels: dict[str, QLabel] = {}

        for cfg in stats_config:
            label = QLabel(f"{cfg['label']}: ")
            self._layout.addWidget(label)
            self.stat_labels[cfg["key"]] = label

        self.hypothesis_result = QLabel("[ ] Hypothesis H₀ not tested")
        self._layout.addWidget(self.hypothesis_result)

    def update_stats(self, result: dict) -> None:
        """
        Update all statistic labels based on result dict.
        """
        for key, label in self.stat_labels.items():
            if key in result and result[key] is not None:
                val = result[key]
                if isinstance(val, float):
                    label.setText(f"{label.text().split(':')[0]}: {val:.4f}")
                else:
                    label.setText(f"{label.text().split(':')[0]}: {val}")
            else:
                label.setText(f"{label.text().split(':')[0]}: N/A")

        if "decision" in result:
            self.update_result(result["decision"])

    def update_result(self, passed: bool) -> None:
        """
        Update hypothesis decision.
        """
        self.hypothesis_result.setText(
            f"[{'✓' if passed else '✗'}] Hypothesis H₀ {'not rejected' if passed else 'rejected'}"
        )

    def clear(self) -> None:
        """
        Reset to default state.
        """
        self.hypothesis_result.setText("[ ] Hypothesis H₀ not tested")
        for key, label in self.stat_labels.items():
            prefix = label.text().split(':')[0]
            label.setText(f"{prefix}: ")

    @abstractmethod
    def get_test_name(self) -> str:
        """
        Get the name of the test for identification.
        Returns:
            str: Name of the homogeneity test.
        """
        pass

    @abstractmethod
    def evaluate(self, samples: list[pd.Series], alpha: float, is_independent: bool) -> None:
        """
        Abstract method to evaluate the homogeneity test with the given samples.
        Args:
            samples (List[pd.Series]): List of samples test.
            alpha (float): Significance level.
            is_independent (bool): True if samples are independent, False if paired.
        """
        pass