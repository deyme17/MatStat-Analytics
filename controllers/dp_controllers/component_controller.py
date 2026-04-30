from typing import Optional, Tuple, List
from enum import Enum, auto
import pandas as pd
import numpy as np
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

        self._orig_full_df_: Optional[pd.DataFrame] = None  # original df
        self.orig_X_df_: Optional[pd.DataFrame] = None      # original df of selected features
        self._bystander_df_: Optional[pd.DataFrame] = None  # df of non-selected columns

        self.pca_labels: Optional[List[str]] = None
        self._state: PCAState = PCAState.IDLE
        self._fitted_ds_name: Optional[str] = None

    def fit(self, X_df: pd.DataFrame) -> None:
        """
        Fit the PCA model to the selected features.
        Args:
            X_df: DataFrame of shape (n_samples, n_selected_features).
        """
        X = X_df.to_numpy(dtype=float)
        self.pca.fit(X)
        self._state = PCAState.FITTED
        self._fitted_ds_name = self.version_manager.get_current_dataset_name()

    def transform(self,
                  X_df: pd.DataFrame,
                  full_df: pd.DataFrame,
                  fit: bool = True,
                  n_components: Optional[int] = None,
                  ev_threshold: Optional[float] = None) -> None:
        """
        Transform selected features with PCA; preserve non-selected columns.\n
        Result column order: [non-selected columns..., PC_1, PC_2, ...]
        Args:
            X_df: DataFrame of selected features (n_samples, n_selected).
            full_df: Full current DataFrame (n_samples, all_features).
            fit: Re-fit PCA before transforming.
            n_components: Number of principal components to keep.
            ev_threshold: Explained-variance threshold for component selection.
        """
        X = X_df.to_numpy(dtype=float)
        if fit:
            X_transformed = self.pca.fit_transform(X, n_components, ev_threshold)
            self._fitted_ds_name = self.version_manager.get_current_dataset_name()
        else:
            X_transformed = self.pca.transform(X, n_components, ev_threshold)

        self.orig_X_df_ = X_df
        self._orig_full_df_ = full_df
        self.pca_labels = [f"PC_{i+1}" for i in range(X_transformed.shape[1])]
        pc_df = pd.DataFrame(X_transformed, columns=self.pca_labels,
                             index=full_df.index)

        # add non-selected columns
        non_selected = [c for c in full_df.columns if c not in X_df.columns]
        if non_selected:
            self._bystander_df_ = full_df[non_selected].reset_index(drop=True)
            new_df = pd.concat([self._bystander_df_, pc_df.reset_index(drop=True)], axis=1)
        else:
            self._bystander_df_ = None
            new_df = pc_df.reset_index(drop=True)

        new_model = self.context.data_model.add_version(new_df, "PCA Transformed")
        self.version_manager.sync_columns(new_model)
        self._state = PCAState.TRANSFORMED
        self._emit()

    def inverse_transform(self, X_df: pd.DataFrame) -> None:
        """
        Reconstruct the original selected features from PC columns;
        re-attach the non-selected (bystander) columns.
        Args:
            X_df: Current DataFrame that contains PC_N columns (and possibly bystanders).
        """
        # select only PC columns
        pc_cols = [c for c in X_df.columns if c in (self.pca_labels or [])]
        if not pc_cols:
            raise ValueError("No PC columns found in the current dataframe.")

        X = X_df[pc_cols].to_numpy(dtype=float)
        X_reconstructed = self.pca.inverse_transform(X)

        reconstructed_df = pd.DataFrame(
            X_reconstructed,
            columns=self.orig_X_df_.columns,
            index=X_df.index,
        ).reset_index(drop=True)

        # restore the prig column order
        if self._bystander_df_ is not None:
            combined = pd.concat(
                [reconstructed_df, self._bystander_df_.reset_index(drop=True)],
                axis=1,
            )
            original_order = [c for c in self._orig_full_df_.columns
                              if c in combined.columns]
            new_df = combined[original_order]
        else:
            new_df = reconstructed_df

        new_model = self.context.data_model.add_version(new_df, "PCA Inv-Transformed")
        self.version_manager.sync_columns(new_model)
        self._state = PCAState.INVERSE_TRANSFORMED
        self._emit()

    def to_original(self) -> None:
        """Revert to the full dataframe as it was before PCA and clear model state."""
        self.pca.clear_state()
        restore_df = self._orig_full_df_ if self._orig_full_df_ is not None else self.orig_X_df_
        orig_model = self.context.data_model.add_version(restore_df, "Reverted to pre-PCA")
        self.version_manager.sync_columns(orig_model)
        self._state = PCAState.IDLE
        self._fitted_ds_name = None
        self._emit()

    def get_explained_variance(self) -> Tuple[float, List[float]]:
        """Return: (Explained Variance, Explained Variance ratio for each component)."""
        explained_variance, evr = self.pca.get_explained_variance()
        return explained_variance, evr.tolist()

    def get_principal_components(self) -> Optional[np.ndarray]:
        return self.pca.principal_components

    def get_eigenvalues(self) -> Optional[np.ndarray]:
        return self.pca.eigenvalues

    def get_eigenvectors(self) -> Optional[np.ndarray]:
        return self.pca.eigenvectors

    def _emit(self) -> None:
        self.event_bus.emit_type(EventType.DATASET_CHANGED)
    
    @property
    def current_state(self) -> PCAState:
        return self._state

    @property
    def fitted_ds_name(self) -> str:
        return self._fitted_ds_name