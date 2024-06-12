import numpy as np
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant


class DetrendedData:
    """
    A class to store the detrended series, the model used for detrending,
    and the type of model ('mean', 'linear', 'quadratic').
    """

    def __init__(self, detrended_series, trend_model, model_type):
        self.detrended_series = detrended_series
        self.trend_model = trend_model
        self.model_type = model_type


def detrend_dataframe(df, column_name="y"):
    """
    Removes the trend from the specified column of a DataFrame using the method
    (mean, linear, quadratic) that results in the lowest AIC value.

    Parameters:
    - df: pandas DataFrame containing the time series data.
    - column_name: string name of the column to detrend.

    Returns:
    - DetrendedData object containing the detrended series, the statistical model,
      and the model type.
    """
    df["t"] = np.array(df["Harvest Year"])

    # Mean method
    mean_model = OLS(df[column_name], np.ones(len(df))).fit()

    # Linear trend model
    X_linear = add_constant(df["t"])
    linear_model = OLS(df[column_name], X_linear).fit()

    # Quadratic trend model
    X_quad = add_constant(np.column_stack((df["t"], df["t"] ** 2)))
    quad_model = OLS(df[column_name], X_quad).fit()

    models = {"mean": mean_model, "linear": linear_model, "quadratic": quad_model}
    best_model_type = min(models, key=lambda x: models[x].aic)
    best_model = models[best_model_type]

    if best_model_type == "mean":
        detrended = df[column_name] - mean_model.predict(np.ones(len(df)))
    elif best_model_type == "linear":
        detrended = df[column_name] - linear_model.predict(X_linear)
    else:  # quadratic
        detrended = df[column_name] - quad_model.predict(X_quad)

    return DetrendedData(detrended, best_model, best_model_type)


def compute_trend(detrended_data, future_time_points=None):
    """
    Adds the trend back to a detrended series, useful for forecasting or visualization.

    Parameters:
    - detrended_data: DetrendedData object containing the detrended series and the model.
    - time_points: Optional numpy array of time points for which to retrend the data.
                   If None, uses the original time points from detrending.

    Returns:
    - The retrended series as a pandas Series.
    """
    # if future_time_points is not of type pandas dataframe then convert it to one
    future_time_points = np.array(future_time_points)

    model_type = detrended_data.model_type[0]
    model = detrended_data.trend_model[0]

    if model_type == "mean":
        trend_component = model.predict(
            np.ones(len(future_time_points)), has_constant="add"
        )
    elif model_type == "linear":
        X_linear = add_constant(future_time_points, has_constant="add")
        trend_component = model.predict(X_linear)
    else:  # quadratic
        X_quad = add_constant(
            np.column_stack((future_time_points, future_time_points**2)),
            has_constant="add",
        )
        trend_component = model.predict(X_quad)

    return trend_component
