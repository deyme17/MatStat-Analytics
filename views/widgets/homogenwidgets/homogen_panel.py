from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from abc import ABC, abstractmethod
from utils.decorators import check_samples, check_independent
import pandas as pd
from utils.ui_styles import groupStyle, groupMargin


class Meta(type(QGroupBox), type(ABC)):
    pass


class BaseHomoTestPanel(QGroupBox, ABC, metaclass=Meta):
    """
    Abstract base class for homogeneity test panels.
    Accepts a dynamic list of statistics for flexible test panels.
    """
    def __init__(self, homogen_controller, stats_config: list[dict], 
                 n_datasets: int, require_independent: bool|None = None) -> None:
        """
        Initialize the panel with given stats configuration.
        Args:
            homogen_controller: Controller for executing tests.
            stats_config (list[dict]): List of dictionaries with keys:
                - "key": str, result dict key
                - "label": str, label prefix
            n_datasets: number of datasets for testing
            require_independent: Does test require dependent or independent samples
                (None if test is applied for both independent and dependent samples)
        """
        super().__init__()
        self.homogen_controller = homogen_controller
        self.n_datasets = n_datasets
        self.require_independent = require_independent

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

    @check_samples
    @check_independent
    def evaluate(self, samples: list[pd.Series], alpha: float, is_independent: bool) -> None:
        """
        Evaluate the test.
        Args:
            samples (list[pd.Series]): List of samples to test (should contain exactly 2 samples).
            alpha (float): Significance level.
            is_independent (bool): True if samples are independent, False if paired.
        """
        result = self.homogen_controller.run_test(
            test_name=self.get_test_name(),
            samples=samples,
            alpha=alpha,
            is_independent=is_independent
        )
        if not result:
            self.clear()
            return

        self.update_stats(result)

    @abstractmethod
    def get_test_name(self) -> str:
        """
        Get the name of the test for identification.
        Returns:
            str: Name of the homogeneity test.
        """
        pass