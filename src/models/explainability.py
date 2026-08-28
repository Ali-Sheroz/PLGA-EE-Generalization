"""Explainability utilities for fitted tree-based PLGA models."""

import numpy as np
import shap


def compute_tree_shap(model, X):
    """Calculate SHAP values for a fitted tree-based estimator.

    SHAP values describe model attribution and must not be interpreted
    as evidence of biological causation.
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)

    return np.asarray(shap_values)


def mean_absolute_shap(shap_values):
    """Calculate mean absolute SHAP attribution for each feature."""
    return np.mean(np.abs(shap_values), axis=0)
