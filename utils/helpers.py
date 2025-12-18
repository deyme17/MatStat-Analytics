import pandas as pd
import re
from typing import List


def get_default_bin_count(df: pd.DataFrame) -> int:
    """Calculate the optimal number of bins for histogram visualization based on data size."""
    if df.empty: return 1
    n = len(df)
    if n <= 100:
        bins = int(n ** 0.5)
    else:
        bins = int(n ** (1 / 3))
    return max(bins, 1)


def validate_feature_names(feature_names: List[str]) -> bool:
    """Validate that feature names"""
    try:
        if not feature_names:
            raise Exception("feature_names cannot be empty")
        if len(feature_names) != len(set(feature_names)):
            raise Exception("feature_names contains duplicate values")
        for name in feature_names:
            pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
            if not bool(re.match(pattern, str(name))):
                raise Exception(f"Invalid feature name format: {name}")
        return True
    except Exception as e:
        print(f"[ValidationError in `validate_feature_names`]: {e}")
        return False