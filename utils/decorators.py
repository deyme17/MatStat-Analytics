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

def require_n_samples(n: int | None = None):
    """
    Decorator to ensure that dataset list has exactly N samples.
    If n is None, requires at least 3 samples.
    """
    def decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            samples = None
            
            if len(args) > 1 and isinstance(args[1], list):
                samples = args[1]
            elif 'samples' in kwargs:
                samples = kwargs['samples']
            
            if samples is None:
                raise ValueError("Could not find 'samples' parameter in method arguments")
            
            count = len(samples)
            
            if n is not None:
                if count != n:
                    if hasattr(self, 'messanger'):
                        self.messanger.show_error(
                            "Test running error",
                            f"This test requires exactly {n} datasets, but {count} were selected."
                        )
                        return None
                    else:
                        raise ValueError(f"This test requires exactly {n} datasets, but {count} were selected.")
            else:
                if count < 3:
                    if hasattr(self, 'messanger'):
                        self.messanger.show_error(
                            "Test running error",
                            "Please select at least three datasets for this method."
                        )
                        return None
                    else:
                        raise ValueError("Please select at least three datasets for this method.")

            return method(self, *args, **kwargs)
        return wrapper
    return decorator