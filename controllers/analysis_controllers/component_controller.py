from typing import Optional, Tuple, List
import pandas as pd
from models.component_analysis import PCA


class ComponentController:
    """
    Main controller class for component analysis.
    """
    def __init__(self, pca: PCA):
        self.pca: PCA = pca
        self.orig_X_df_: Optional[pd.DataFrame] = None
        self.pca_labels: Optional[List[str]] = None

    def fit(self, X_df: pd.DataFrame) -> None:
        """
        Fit the PCA model to the data.
        Args:
            X (np.ndarray): Data of shape (n_samples, n_features).
        """
        X = X_df.to_numpy(dtype=float)
        self.pca.fit(X)

    def transform(self, X_df: pd.DataFrame,
                 fit: bool = True,
                 n_components: Optional[int] = None,
                 ev_threshold: Optional[float] = None) -> pd.DataFrame:
        """
        Tranform X dataframe using PCA model.
        Args:
            X_df (pd.DataFrame): Dataframe of shape (n_samples, n_features).
            fit (bool): Fit the PCA model before transform.
            n_components (int|None): Number of principal components.
            evr_threshold (float|None): Explained variance threshold,
                    that is used for principal components selection.
        Returns:
            pd.DataFrame: Transformed dataframe of shape (n_samples, n_components).
        """
        X = X_df.to_numpy(dtype=float)

        X_transformed = None
        if fit:
            X_transformed = self.pca.fit_transform(X, n_components, ev_threshold)
        else:
            X_transformed = self.pca.transform(X, n_components, ev_threshold)

        self.orig_X_df_ = X_df
        self.pca_labels = [f"PC_{i+1}" for i in range(X_transformed.shape[1])]
        return pd.DataFrame(X_transformed, columns=self.pca_labels)
    
    def inverse_transform(self, X_df: pd.DataFrame):
        """
        Apply inverse PCA transform to dataframe.
        Args:
            X (pd.DataFrame): Dataframe of shape (n_samples, n_components).
        Returns:
            pd.DataFrame: Reconstructed dataframe of shape (n_samples, n_features).
        """
        X = X_df.to_numpy(dtype=float)
        X_reconstructed = self.pca.inverse_transform(X)
        return pd.DataFrame(X_reconstructed, columns=self.orig_X_df_.columns, index=X_df.index)

    def get_explained_variance(self) -> Tuple[float, List[float]]:
        """Return: (Explained Variance, Explained Variance ratio for each component)."""
        explained_variance, evr = self.pca.get_explained_variance()
        return explained_variance, evr.tolist()
    
    def to_original(self) -> pd.DataFrame:
        """Return original X_df and clear PCA model state."""
        self.pca.clear_state()
        return self.orig_X_df_