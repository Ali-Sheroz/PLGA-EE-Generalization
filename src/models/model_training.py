"""Model definitions for PLGA encapsulation-efficiency prediction."""

from sklearn.compose import TransformedTargetRegressor
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from xgboost import XGBRegressor


RANDOM_STATE = 42


def build_models(preprocessor):
    """Return the candidate regression models and reference predictor."""

    linear = Pipeline(
        [
            ("preprocessing", preprocessor),
            ("model", LinearRegression()),
        ]
    )

    random_forest = Pipeline(
        [
            ("preprocessing", preprocessor),
            (
                "model",
                RandomForestRegressor(
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    xgboost = Pipeline(
        [
            ("preprocessing", preprocessor),
            (
                "model",
                XGBRegressor(
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    svr_pipeline = Pipeline(
        [
            ("preprocessing", preprocessor),
            ("model", SVR(kernel="rbf")),
        ]
    )

    svr = TransformedTargetRegressor(
        regressor=svr_pipeline,
        transformer=StandardScaler(),
    )

    dummy = DummyRegressor(strategy="mean")

    return {
        "Linear Regression": linear,
        "Random Forest": random_forest,
        "XGBoost": xgboost,
        "SVR (RBF)": svr,
        "Mean Predictor": dummy,
    }
