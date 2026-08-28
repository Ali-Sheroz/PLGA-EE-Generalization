"""Preprocessing utilities for PLGA-EE-Generalization.

Reusable preprocessing components for the PLGA encapsulation-efficiency
generalization study. Preprocessing should be fitted inside each training
fold during grouped cross-validation to prevent leakage.
"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_preprocessor(continuous_features, categorical_features):
    """Create the preprocessing transformer used for model development.

    Continuous variables are standardized and categorical variables are
    one-hot encoded. The transformer must be fitted only on training data
    within each cross-validation fold.
    """
    return ColumnTransformer(
        transformers=[
            ("continuous", StandardScaler(), continuous_features),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
        ],
        remainder="drop",
    )
