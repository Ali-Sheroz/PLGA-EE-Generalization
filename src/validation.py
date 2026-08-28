"""Grouped-validation utilities for unseen-drug evaluation."""

import numpy as np
from sklearn.model_selection import GroupKFold


def check_group_separation(train_index, test_index, groups):
    """Verify that no drug group occurs in both training and test sets."""
    groups = np.asarray(groups)

    train_groups = set(groups[train_index])
    test_groups = set(groups[test_index])

    overlap = train_groups.intersection(test_groups)

    if overlap:
        raise ValueError(
            f"Drug-group leakage detected. Overlapping groups: {overlap}"
        )

    return True


def grouped_cv_splits(X, groups, n_splits=5):
    """Generate leakage-checked GroupKFold splits by drug identity."""
    splitter = GroupKFold(n_splits=n_splits)

    for train_index, test_index in splitter.split(X, groups=groups):
        check_group_separation(
            train_index=train_index,
            test_index=test_index,
            groups=groups,
        )

        yield train_index, test_index
