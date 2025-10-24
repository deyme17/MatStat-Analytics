from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QComboBox, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem
)
from utils import AppContext
from services import UIMessager
from controllers import ParameterEstimation

from models.data_model import DataModel
from models.stat_distributions import registered_distributions
from models.params_estimators import registered_estimation_methods


class ParamEstimationTab(QWidget):
    """
    Tab widget for estimating distribution parameters using different methods.
    Uses AppContext for dependencies.
    """
    def __init__(self, context: AppContext, estimator: ParameterEstimation):
        """
        Args:
            context: AppContext with data_model and messanger
            estimator: Parameters estimation implementation
        """
        super().__init__()
        self.messanger: UIMessager = context.messanger
        self.data_model: DataModel = context.data_model
        self.estimator: ParameterEstimation = estimator
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize and layout all UI components."""
        layout = QVBoxLayout()

        # Distribution selection
        self.dist_combo = QComboBox()
        self.dist_combo.addItems(registered_distributions.keys())

        # Method selection
        self.method_combo = QComboBox()
        self.method_combo.addItems(registered_estimation_methods.keys())

        # Estimation button
        self.estimate_button = QPushButton("Estimate Parameters")
        self.estimate_button.clicked.connect(self._handle_estimation)

        # Results table
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["Parameter", "Estimated Value"])

        # Assemble layout
        layout.addWidget(QLabel("Select Distribution:"))
        layout.addWidget(self.dist_combo)
        layout.addWidget(QLabel("Select Estimation Method:"))
        layout.addWidget(self.method_combo)
        layout.addWidget(self.estimate_button)
        layout.addWidget(self.result_table)
        self.setLayout(layout)

    def _handle_estimation(self) -> None:
        """Handle parameter estimation request."""
        if not self.data_model or not self.messanger:
            return

        data = self.data_model.series
        if data is None:
            self.messanger.show_error("No Data", "No data available for estimation")
            return

        if data.empty or data.isna().all():
            self.messanger.show_error("Invalid Data", "Data contains no valid values")
            return

        dist_name = self.dist_combo.currentText()
        method_name = self.method_combo.currentText()

        try:
            # Get distribution class
            dist_class = registered_distributions.get(dist_name)
            if not dist_class:
                self.messanger.show_error("Invalid Distribution", 
                    f"Unknown distribution: {dist_name}")
                return

            # Estimate parameters
            params = self.estimator.estimate(dist_name, method_name, data)
            if params is None:
                self.messanger.show_error("Estimation Failed", 
                    f"Failed to estimate parameters for {dist_name}")
                return

            # Display results
            self._display_results(dist_class(), params)

        except Exception as e:
            self.messanger.show_error("Estimation Error", 
                f"Error during estimation: {str(e)}")

    def _display_results(self, distribution, params: list) -> None:
        """Display estimated parameters in the results table."""
        param_names = list(distribution.distribution_params.keys())
        self.result_table.setRowCount(len(params))
        
        for i, (name, value) in enumerate(zip(param_names, params)):
            self.result_table.setItem(i, 0, QTableWidgetItem(name))
            self.result_table.setItem(i, 1, QTableWidgetItem(f"{value:.4f}"))

    def clear_results(self) -> None:
        """Clear the results table."""
        self.result_table.setRowCount(0)