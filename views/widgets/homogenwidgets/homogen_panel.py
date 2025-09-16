from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QWidget
from abc import ABC, abstractmethod
import pandas as pd
from utils.ui_styles import groupStyle, groupMargin


class Meta(type(QGroupBox), type(ABC)):
    pass

class BaseHomoTestPanel(QGroupBox, ABC, metaclass=Meta):
    """
    Abstract base class for homogeneity test panels used in the application.
    Provides a common layout and logic for displaying homogeneity test results.
    """
    def __init__(self, homogen_controller) -> None:
        """
        Initialize the homogeneity test panel.
        Args:
            homogen_controller (HomogenController): Controller for executing homogeneity tests.
        """
        super().__init__()
        self.homogen_controller = homogen_controller
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
        Returns:
            QLabel: The created label widget.
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

    def clear(self) -> None:
        """
        Reset the panel to the default untested state.
        """
        self.hypothesis_result.setText("[ ] Hypothesis H₀ not tested")
        for i in range(self._layout.count()):
            widget = self._layout.itemAt(i).widget()
            if isinstance(widget, QLabel) and widget != self.hypothesis_result:
                text = widget.text()
                if ':' in text:
                    prefix = text.split(':')[0] + ': '
                    widget.setText(prefix)