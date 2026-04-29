from typing import Optional, Tuple, List
from enum import Enum, auto
import pandas as pd
from models.component_analysis import PCA
from services import DataVersionManager
from utils import AppContext, EventBus, EventType



class PCAState(Enum):
    IDLE = auto()                   # no fit yet
    FITTED = auto()                 # fit done, not transformed
    TRANSFORMED = auto()            # transform done
    INVERSE_TRANSFORMED = auto()    # inverse transform done


class ComponentController:
    """
    Main controller class for component analysis.
    """
    def __init__(self, context: AppContext, pca: PCA):
        self.pca: PCA = pca
        self.context: AppContext = context
        self.event_bus: EventBus = context.event_bus
        self.version_manager: DataVersionManager = context.version_manager
        self.orig_X_df_: Optional[pd.DataFrame] = None
        self.pca_labels: Optional[List[str]] = None
        self._state: PCAState = PCAState.IDLE
        self._fitted_ds_name: Optional[str] = None

    def fit(self, X_df: pd.DataFrame) -> None:
        """
        Fit the PCA model to the data.
        Args:
            X (np.ndarray): Data of shape (n_samples, n_features).
        """
        X = X_df.to_numpy(dtype=float)
        self.pca.fit(X)
        self._state = PCAState.FITTED
        self._fitted_ds_name = self.version_manager.get_current_dataset_name()

    def transform(self, X_df: pd.DataFrame,
                 fit: bool = True,
                 n_components: Optional[int] = None,
                 ev_threshold: Optional[float] = None) -> None:
        """
        Tranform X dataframe using PCA model.
        Args:
            X_df (pd.DataFrame): Dataframe of shape (n_samples, n_features).
            fit (bool): Fit the PCA model before transform.
            n_components (int|None): Number of principal components.
            evr_threshold (float|None): Explained variance threshold,
                    that is used for principal components selection.
        """
        X = X_df.to_numpy(dtype=float)

        X_transformed = None
        if fit:
            X_transformed = self.pca.fit_transform(X, n_components, ev_threshold)
            self._fitted_ds_name = self.version_manager.get_current_dataset_name()
        else:
            X_transformed = self.pca.transform(X, n_components, ev_threshold)

        self.orig_X_df_ = X_df
        self.pca_labels = [f"PC_{i+1}" for i in range(X_transformed.shape[1])]

        new_df = pd.DataFrame(X_transformed, columns=self.pca_labels)
        new_model = self.context.data_model.add_version(new_df, "PCA Transformed")

        self.version_manager.sync_columns(new_model)
        self._state = PCAState.TRANSFORMED
        self._emit()
    
    def inverse_transform(self, X_df: pd.DataFrame):
        """
        Apply inverse PCA transform to dataframe.
        Args:
            X (pd.DataFrame): Dataframe of shape (n_samples, n_components).
        """
        X = X_df.to_numpy(dtype=float)
        X_reconstructed = self.pca.inverse_transform(X)

        new_df = pd.DataFrame(X_reconstructed, columns=self.orig_X_df_.columns, index=X_df.index)
        new_model = self.context.data_model.add_version(new_df, "PCA Inv-Transformed")

        self.version_manager.sync_columns(new_model)
        self._state = PCAState.INVERSE_TRANSFORMED
        self._emit()
    
    def to_original(self) -> None:
        """Revert original X_df and clear PCA model state."""
        self.pca.clear_state()
        orig_model = self.context.data_model.add_version(self.orig_X_df_, "Reverted to pre-PCA")

        self.version_manager.sync_columns(orig_model)
        self._state = PCAState.IDLE
        self._fitted_ds_name = None
        self._emit()

    def get_explained_variance(self) -> Tuple[float, List[float]]:
        """Return: (Explained Variance, Explained Variance ratio for each component)."""
        explained_variance, evr = self.pca.get_explained_variance()
        return explained_variance, evr.tolist()

    def _emit(self) -> None:
        self.event_bus.emit_type(EventType.DATASET_CHANGED)

    @property
    def current_state(self) -> PCAState:
        return self._state
    
    @property
    def fitted_ds_name(self) -> str:
        return self._fitted_ds_name