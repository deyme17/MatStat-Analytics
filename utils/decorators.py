import functools
import pandas as pd


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