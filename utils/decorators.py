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


def check_samples(method):
    """Ensure the correct number of datasets is selected, using self.n_datasets."""
    @functools.wraps(method)
    def wrapper(self, samples, *args, **kwargs):
        count = len(samples)
        n = getattr(self, "n_datasets", None)
        if n is not None:
            if count != n:
                raise ValueError(f"{self.get_test_name()} requires exactly {n} datasets, but {count} were selected.")
        else:
            if count < 3:
                raise ValueError(f"{self.get_test_name()} requires at least 3 datasets, but {count} were selected.")
        return method(self, samples, *args, **kwargs)
    return wrapper


def check_independent(method):
    """
    Ensure independence requirement is met, using self.require_independent.
    If self.require_independent is True, samples must be independent.
    """
    @functools.wraps(method)
    def wrapper(self, samples, alpha, is_independent, *args, **kwargs):
        req = getattr(self, "require_independent", None)
        if req is True and not is_independent:
            raise ValueError(f"{self.get_test_name()} requires independent samples.")
        return method(self, samples, alpha, is_independent, *args, **kwargs)
    return wrapper