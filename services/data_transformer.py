from services.transformation_service import TransformationService

class DataTransformer:
    def __init__(self):
        self.transformed_data = None
        self.transformation_steps = []
        self.current_transformation = "Original"

    def standardize(self, data):
        self.transformed_data = TransformationService.standardize(data)
        self._add_step("Standardized")
        return self.transformed_data

    def log_transform(self, data):
        self.transformed_data = TransformationService.log_transform(data)
        self._add_step("Log Transform")
        return self.transformed_data

    def shift(self, data, value):
        self.transformed_data = TransformationService.shift(data, value)
        self._add_step(f"Shifted by {value}")
        return self.transformed_data

    def _add_step(self, label):
        self.transformation_steps.append(label)
        self.current_transformation = self._format_transformation()

    def reset(self):
        self.transformed_data = None
        self.transformation_steps = []
        self.current_transformation = "Original"

    def _format_transformation(self):
        if not self.transformation_steps:
            return "Original"
        if len(self.transformation_steps) <= 3:
            return " → ".join(self.transformation_steps)
        return " → ".join(self.transformation_steps[:2]) + f" → ... → {self.transformation_steps[-1]}"

    def get_state(self):
        return {
            'transformed_data': self.transformed_data.copy() if self.transformed_data is not None else None,
            'transformation_steps': list(self.transformation_steps),
            'current_transformation': self.current_transformation
        }

    def load_state(self, state):
        self.transformed_data = state['transformed_data']
        self.transformation_steps = list(state['transformation_steps'])
        self.current_transformation = state['current_transformation']