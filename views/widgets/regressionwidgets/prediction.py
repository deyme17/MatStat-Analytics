import pandas as pd
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from services.ui_services.messager import UIMessager
from controllers import RegressionController
from utils import AppContext
from utils.ui_styles import groupMargin, groupStyle
from views.widgets.utils import create_section_header, make_button
from views.widgets.regressionwidgets.subwidgets import RegrInputsWidget, RegrPredictionOutputWidget

DEFAULT_ALPHA = 0.05


class RegrPredictionWidget(QWidget):
    """Widget for making predictions for new data using fitted model."""
    def __init__(self, context: AppContext, regr_controller: RegressionController):
        super().__init__()
        self.context: AppContext = context
        self.messanger: UIMessager = context.messanger
        self.controller: RegressionController = regr_controller
        self.alpha: float = DEFAULT_ALPHA
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize regression prediction UI components."""
        self.setStyleSheet(groupStyle + groupMargin)
        layout = QVBoxLayout(self)

        layout.addLayout(create_section_header("Prediction Section"))

        self.inputs_widget = RegrInputsWidget()
        layout.addWidget(self.inputs_widget)

        self.predict_btn = make_button("Predict", callback=self._predict, height=32)
        layout.addWidget(self.predict_btn)

        self.output_widget = RegrPredictionOutputWidget()
        layout.addWidget(self.output_widget)

    def setup_for_model(self, feature_names: list[str]) -> None:
        """Setup input fields based on fitted model features."""
        self.inputs_widget.setup_features(feature_names)

    def set_alpha_value(self, alpha: float) -> None:
        """Set a new alpha (significance level) value."""
        self.alpha = alpha

    def _predict(self) -> None:
        """Execute regression model prediction and show results."""
        input_data = self.inputs_widget.parse_input_data(self.messanger)
        if input_data is None:
            return

        try:
            X_df = pd.DataFrame([input_data])
            prediction = self.controller.predict(X_df)
            intervals = self.controller.predict_intervals(X_df, self.alpha)

            self.output_widget.display_success(prediction.iloc[0], intervals)
        except Exception as e:
            self.messanger.show_error("Prediction error", str(e))
            self.output_widget.display_error()

    def clear(self) -> None:
        """Clear all input fields and results."""
        self.inputs_widget.clear()
        self.output_widget.clear()