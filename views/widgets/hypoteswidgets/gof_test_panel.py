from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QWidget
from abc import ABC, abstractmethod
import pandas as pd

from utils.ui_styles import groupStyle, groupMargin
from models.stat_distributions.stat_distribution import StatisticalDistribution


class Meta(type(QGroupBox), type(ABC)):
    pass

class BaseTestPanel(QGroupBox, ABC, metaclass=Meta):
    """
    Abstract base class for statistical test panels used in the application.
    Provides a common layout and logic for displaying hypothesis test results.
    """
    def __init__(self, title: str, gof_controller) -> None:
        """
        Initialize the test panel group box with a title and base layout.
        Args:
            title (str): Title of the group box representing the test.
            gof_controller (GOFController): Controller for executing Goodness-of-Fit tests.
        """
        super().__init__(title)
        self.gof_controller = gof_controller
        self.setCheckable(False)
        self.setStyleSheet(groupStyle + groupMargin)

        self.hypothesis_result: QLabel = QLabel("[ ] Hypothesis H₀ not tested")
        self._layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self._layout)

    def add_stat_label(self, prefix: str = " ") -> QLabel:
        """
        Adds a QLabel to the layout for displaying test statistics.
        Args:
            prefix (str): Text prefix for the label.
        """
        label = QLabel(prefix)
        self._layout.addWidget(label)
        return label

    def finalize_layout(self, *extra_widgets: QWidget) -> None:
        """
        Finalize layout by appending any extra widgets and the result label.
        Args:
            *extra_widgets (QWidget): Optional widgets to add before the result.
        """
        for widget in extra_widgets:
            self._layout.addWidget(widget)
        self._layout.addWidget(self.hypothesis_result)

    def update_result(self, passed: bool) -> None:
        """
        Update the hypothesis result label based on the test outcome.
        Args:
            passed (bool): True if H₀ is not rejected, False if rejected.
        """
        self.hypothesis_result.setText(
            f"[{'✓' if passed else '✗'}] Hypothesis H₀ {'not rejected' if passed else 'rejected'}"
        )

    @abstractmethod
    def evaluate(self, data: pd.Series, dist: StatisticalDistribution, alpha: float) -> None:
        """
        Abstract method to evaluate the test with the given data and distribution.
        Args:
            data (pd.Series): Sample data to evaluate.
            dist (StatisticalDistribution): Fitted distribution to compare against.
            alpha (float): Significance level.
        """
        pass

    def clear(self) -> None:
        """
        Reset the panel to the default untested state.
        """
        self.hypothesis_result.setText("[ ] Hypothesis H₀ not tested")