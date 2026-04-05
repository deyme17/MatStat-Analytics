from .base_dp_widget import BaseDataWidget
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QDoubleSpinBox
from controllers import DataTransformController
from utils import EventBus, EventType
from .subwidgets.standardize_dialog import StandardizeDialog
from .subwidgets.log_dialog import LogTransformDialog

MIN_SHIFT, MAX_SHIFT = -1000, 1000
SHIFT_STEP = 1
DEFAULT_SHIFT = 0


class TransformDataWidget(BaseDataWidget):
    """Widget for performing basic data transformations."""
    def __init__(self, controller: DataTransformController, event_bus: EventBus):
        buttons_config = [
            ("standardize_button", "Standardize",  self._on_standardize),
            ("log_button",         "Log Transform", self._on_log_transform),
            ("shift_button",       "Shift Data",
             lambda: controller.shift_data(self.shift_spinbox.value())),
        ]
        super().__init__("Process Data", controller, event_bus, buttons_config)
        self._setup_shift_spinbox()
        self._subscribe_to_events()

    def _subscribe_to_events(self) -> None:
        self.event_bus.subscribe(EventType.MISSING_VALUES_DETECTED, self._disable_widget)
        self.event_bus.subscribe(EventType.MISSING_VALUES_HANDLED,  self._unable_widget)

    def _setup_shift_spinbox(self) -> None:
        """Setup shift spinbox below the buttons."""
        shift_layout = QHBoxLayout()
        self.shift_label   = QLabel("Shift by:")
        self.shift_spinbox = QDoubleSpinBox()
        self.shift_spinbox.setRange(MIN_SHIFT, MAX_SHIFT)
        self.shift_spinbox.setSingleStep(SHIFT_STEP)
        self.shift_spinbox.setValue(DEFAULT_SHIFT)
        self.shift_spinbox.setEnabled(True)
        shift_layout.addWidget(self.shift_label)
        shift_layout.addWidget(self.shift_spinbox)
        self.add_layout(shift_layout)

    def _on_standardize(self) -> None:
        """Open StandardizeDialog, then call controller."""
        model = self.controller.context.data_model
        if not model:
            return

        dlg = StandardizeDialog(
            dataframe=model.dataframe,
            std_params=self.controller.std_params,
            parent=self,
        )
        if dlg.exec() != dlg.DialogCode.Accepted:
            return

        if dlg.action == "normalize":
            self.controller.standardize_data(columns=dlg.selected_columns)
        elif dlg.action == "unnormalize":
            self.controller.unstandardize_data()

    def _on_log_transform(self) -> None:
        """Open LogTransformDialog, then call the appropriate controller method."""
        dlg = LogTransformDialog(parent=self)
        if dlg.exec() != dlg.DialogCode.Accepted:
            return

        kind = dlg.kind          # 'ln' | 'lg' | 'log2'
        inverse = dlg.inverse    # bool

        if inverse:
            self.controller.inverse_log_transform_data(kind=kind)
        else:
            self.controller.log_transform_data(kind=kind)