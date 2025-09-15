import functools
import pandas as pd
from models.data_model import DataModel


def require_one_dimensional_dataframe(method):
    """
    Decorator to ensure self.context.data_model.dataframe is one-dimensional.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        df: pd.DataFrame = getattr(self.context.data_model, "dataframe", None)

        if df is None:
            raise RuntimeError("Dataframe is None.")

        if not isinstance(df, pd.DataFrame):
            raise TypeError("Expected a pandas DataFrame in context.data_model.dataframe.")

        if df.shape[1] != 1:
            if hasattr(self.context, "messanger"):
                self.context.messanger.show_error(
                    "Dimension Error",
                    "Expected a 1D dataframe (single column)."
                )
                return
            else:
                raise RuntimeError("Expected a 1D dataframe (single column).")

        return method(self, *args, **kwargs)
    return wrapper

def require_n_samples(method, n: int | None = None):
    """
    Decorator to ensure that dataset list has exactly N samples.
    If n is None, requires at least 3 sample.
    """
    @functools.wraps(method)
    def wrapper(self, selected_models: dict[str, DataModel], *args, **kwargs):
        count = len(selected_models)
        if n is not None:
            if count != n:
                self.messanger.show_error(
                    "Test running error",
                    f"This test requires exactly {n} datasets, but {count} were selected."
                )
                return
        else:
            if count < 3:
                self.messanger.show_error(
                    "Test running error",
                    "Please select at least three dataset for this method."
                )
                return

        return method(self, selected_models, *args, **kwargs)
    return wrapper
