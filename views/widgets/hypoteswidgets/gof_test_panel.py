from PyQt6.QtWidgets import QGroupBox, QLabel, QVBoxLayout
from utils.ui_styles import groupStyle, groupMargin

class BaseTestPanel(QGroupBox):
    """
    Abstract base class for statistical test panels used in the application.
    Provides common layout and logic for displaying hypothesis test results.

    Attributes:
        window (QMainWindow): Reference to the main application window.
        hypothesis_result (QLabel): Displays the status of the null hypothesis.
        _layout (QVBoxLayout): Vertical layout container for the panel's widgets.
    """

    def __init__(self, title, window):
        """
        Initializes the test panel group box with a title and base layout.

        Args:
            title (str): Title of the group box representing the test.
            window (QMainWindow): Main application window reference.
        """
        super().__init__(title)
        self.window = window
        self.setCheckable(False)
        self.setStyleSheet(groupStyle + groupMargin)

        self.hypothesis_result = QLabel("[ ] Hypothesis H₀ not tested")
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

    def add_stat_label(self, prefix: str = " "):
        """
        Adds a label to the layout for displaying a test statistic or value.

        Args:
            prefix (str): Text prefix for the label.

        Returns:
            QLabel: The newly created label.
        """
        label = QLabel(prefix)
        self._layout.addWidget(label)
        return label

    def finalize_layout(self, *extra_widgets):
        """
        Finalizes the layout by appending extra widgets (if any) and
        the hypothesis result label.

        Args:
            *extra_widgets: Any additional widgets to include before the result label.
        """
        for w in extra_widgets:
            self._layout.addWidget(w)
        self._layout.addWidget(self.hypothesis_result)

    def update_result(self, passed: bool):
        """
        Updates the hypothesis result label based on test outcome.

        Args:
            passed (bool): True if H₀ is not rejected, False otherwise.
        """
        self.hypothesis_result.setText(
            f"[{'✓' if passed else '✗'}] Hypothesis H₀ {'not rejected' if passed else 'rejected'}"
        )

    def evaluate(self, data, dist, alpha):
        """
        Abstract method to perform the test evaluation.

        Args:
            data (pd.Series): Sample data to evaluate.
            dist (StatisticalDistribution): Theoretical distribution to test against.
            alpha (float): Significance level.

        Raises:
            NotImplementedError: If not overridden in the subclass.
        """
        raise NotImplementedError("Subclasses must implement evaluate()")

    def clear(self):
        """
        Resets the hypothesis result label to the default untested state.
        """
        self.hypothesis_result.setText("[ ] Hypothesis H₀ not tested")