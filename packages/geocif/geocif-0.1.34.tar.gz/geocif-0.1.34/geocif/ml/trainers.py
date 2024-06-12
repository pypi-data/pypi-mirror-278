import multiprocessing as mp

import numpy as np
import optuna
from catboost import CatBoostRegressor
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def loocv(
    model,
    df,
    loocv_var,
    feature_names,
    target_col,
    fraction_loocv=1.0,
    cat_features=[],
    trial_id=0,
):
    """
    Perform Leave-One-Out Cross Validation (LOOCV)
    :param model: CatBoostRegressor, CatBoost model
    :param df: pd.DataFrame, training data
    :param loocv_var: str, variable to perform LOOCV on
    :param feature_names: list, list of feature names
    :param target_col: str, target column name
    :param fraction_loocv: float, fraction of unique values to perform LOOCV on
    :param cat_features: list, list of categorical feature names
    :return: float, average RMSE
    """
    rmse_values = []

    X = df[feature_names + cat_features]
    y = df[target_col]

    # Perform LOOCV based on precentage of loocv_var
    # Find unique values
    unique_values = df[loocv_var].unique()
    num_to_select = int(len(unique_values) * fraction_loocv)
    # Randomly select X% of the unique values without replacement
    selected_values = np.random.choice(unique_values, size=num_to_select, replace=False)
    pbar = tqdm(selected_values, leave=False)
    for idx, var in enumerate(pbar):
        pbar.set_description(f"Trial {trial_id}, LOOCV {var}")
        pbar.update()

        train_index = df[df[loocv_var] != var].index
        val_index = df[df[loocv_var] == var].index

        X_train, X_val = X.loc[train_index], X.loc[val_index]
        y_train, y_val = y.loc[train_index], y.loc[val_index]

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_val)

        # Calculate RMSE
        rmse = root_mean_squared_error(y_val, y_pred)
        rmse_values.append(rmse)

    # Compute average MSE
    average_rmse = np.mean(rmse_values)

    return average_rmse


def optuna_objective(model, df, feature_names, target_col, cat_features=[]):
    """

    Args:
        model:
        df:
        feature_names:
        target_col:
        cat_features:

    Returns:

    """
    X = df[feature_names + cat_features]
    y = df[target_col]

    # Divide the data into training and validation sets
    train_X, val_X, train_y, val_y = train_test_split(
        X, y, test_size=0.2, random_state=0
    )

    model.fit(
        train_X,
        train_y,
        cat_features=cat_features,
        eval_set=(val_X, val_y),
        early_stopping_rounds=100,
        use_best_model=True,
        verbose=False,
    )

    # Make predictions
    val_preds = model.predict(val_X)

    # Evaluate predictions
    rmse = root_mean_squared_error(val_y, val_preds)

    return rmse


def optimized_model(
    model_name,
    df,
    use_loocv,
    loocv_var,
    feature_names,
    target_col,
    fraction_loocv,
    cat_features=[],
    seed=0,
):
    """
    Train CatBoost model using Optuna hyperparameter optimization
    :param model_name: str, 'CatBoost' or 'XGBoost'
    :param df: pd.DataFrame, training data
    :param loocv_var: str, 'Harvest Year'
    :param feature_names: list, list of feature names
    :param target_col: str, target column name
    :param fraction_loocv: float, fraction of unique values to perform LOOCV on
    :param cat_features: list, list of categorical feature names
    :param seed: int, random seed
    """
    # Define objecive function for optuna Hyperparameter tuning
    def _optuna_objective(trial):
        try:
            if model_name == "catboost":
                params = {
                    "depth": trial.suggest_int("depth", 1, 7),
                    "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1),
                    "iterations": trial.suggest_int(
                        "iterations", low=1000, high=5000, step=500
                    ),
                    "subsample": trial.suggest_float("subsample", 1.0, 1.0),
                    "random_strength": trial.suggest_float("random_strength", 0.3, 1.0),
                    "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 1.0),
                    "loss_function": "MAPE",
                    "early_stopping_rounds": 50,
                    "random_seed": seed,
                    "verbose": False,
                }

                # Fit the optuna model
                optuna_model = CatBoostRegressor(**params, cat_features=cat_features)
            else:
                raise NotImplementedError

            if use_loocv:
                trial_id = trial.number
                error_metric = loocv(
                    optuna_model,
                    df,
                    loocv_var,
                    feature_names,
                    target_col,
                    fraction_loocv,
                    cat_features,
                    trial_id,
                )
            else:
                error_metric = optuna_objective(
                    optuna_model, df, feature_names, target_col, cat_features
                )

            return error_metric
        except Exception as e:
            print(f"Trial failed with exception: {e}")
            return np.inf  # Assign a high cost to failed trials

    try:
        # Optimize hyperparameters
        n_trials = min(20, int(mp.cpu_count() * 0.9))
        optuna.logging.set_verbosity(optuna.logging.WARNING)  # Disable verbose
        sampler = optuna.samplers.TPESampler(seed=seed)
        study = optuna.create_study(sampler=sampler, direction="minimize")
        study.optimize(
            _optuna_objective, n_trials=n_trials, n_jobs=int(mp.cpu_count() * 0.4)
        )
        if study.best_trial is None:
            raise ValueError("Optimization failed to complete any trials.")
        hyperparams = study.best_trial.params

    except Exception as e:
        print(f"Optimization failed: {e}")
        hyperparams = {
            "depth": 6,
            "learning_rate": 0.01,
            "iterations": 10,
            "subsample": 1.0,
            "random_strength": 0.5,
            "reg_lambda": 0.001,
            "loss_function": "MAPE",
            "early_stopping_rounds": 50,
            "random_seed": seed,
            "verbose": False,
        }

    # Model Initialization & Training
    if model_name == "catboost":
        model = CatBoostRegressor(**hyperparams, cat_features=cat_features)
    else:
        raise NotImplementedError

    return hyperparams, model


def auto_train(
    cluster_strategy,
    model_name,
    use_loocv,
    loocv_var,
    df_train,
    X_train,
    y_train,
    feature_names,
    target_col,
    optimize=False,
    fraction_loocv=1.0,
    cat_features=[],
    monotonic_fatures=[],
    seed=0,
):
    """
    Train CatBoost model using Optuna hyperparameter optimization

    :param cluster_strategy: str, 'individual' or 'auto_detect' or 'single'
    :param model_name: str, 'CatBoost' or 'XGBoost'
    :param stage: int, 'Dekad'
    :param loocv_var: str, 'Harvest Year'
    :param df_train: pd.DataFrame, training data
    :param feature_names: list, list of feature names
    :param target_col: str, target column name
    :param optimize: bool, whether to optimize hyperparameters
    :param fraction_loocv: float, fraction of unique values to perform LOOCV on
    :param cat_features: list, list of categorical feature names
    :param seed: int, random seed
    """
    if optimize:
        hyperparams, model = optimized_model(
            model_name,
            df_train,
            use_loocv,
            loocv_var,
            feature_names,
            target_col,
            fraction_loocv,
            cat_features,
            seed,
        )
    else:
        hyperparams = {}

        if model_name in ["catboost", "merf"]:
            hyperparams = {
                "depth": 6,
                "learning_rate": 0.01,
                "iterations": 5000,
                "subsample": 1.0,
                "random_strength": 0.5,
                "reg_lambda": 0.001,
                "loss_function": "MAPE",
                "early_stopping_rounds": 50,
                "random_seed": seed,
                "verbose": False,
            }
            if model_name == "catboost":
                model = CatBoostRegressor(**hyperparams, cat_features=cat_features)
            elif model_name == "merf":
                from merf import MERF

                hyperparams["iterations"] = 1000
                regr = CatBoostRegressor(**hyperparams, cat_features=cat_features)
                model = MERF(regr, max_iterations=10)
        elif model_name == "linear":
            from sklearn.linear_model import LassoCV

            model = LassoCV(cv=5, random_state=42)
        elif model_name == "gam":
            from pygam import LinearGAM

            model = LinearGAM(n_splines=25, spline_order=3).gridsearch(
                X_train.values, y_train.values, lam=np.logspace(-3, 3, 11)
            )
        elif model_name == "geospaNN":
            import torch
            import geospaNN

            # Remove any categorical features
            X_train = X_train.drop(columns=cat_features)
            X = torch.from_numpy(X_train.to_numpy()).float()
            Y = torch.from_numpy(y_train.to_numpy().reshape(-1)).float()

            coord = torch.from_numpy(df_train[['lon', 'lat']].to_numpy()).float()

            p = X.shape[1]
            n = X.shape[0]
            nn = 5

            data = geospaNN.make_graph(X, Y, coord, nn)

            mlp = torch.nn.Sequential(
                torch.nn.Linear(p, 50),
                torch.nn.ReLU(),
                torch.nn.Linear(50, 20),
                torch.nn.ReLU(),
                torch.nn.Linear(20, 10),
                torch.nn.ReLU(),
                torch.nn.Linear(10, 1),
            )

            # Split data
            data_train, data_val, data_test = geospaNN.split_data(X, Y, coord, neighbor_size=nn, test_proportion=0.1)
            theta0 = geospaNN.theta_update(torch.tensor([1, 1.5, 0.01]), mlp(data_train.x).squeeze() - data_train.y, data_train.pos, neighbor_size=5)
            model = geospaNN.nngls(p=p, neighbor_size=nn, coord_dimensions=2, mlp=mlp, theta=torch.tensor(theta0))
            nngls_model = geospaNN.nngls_train(model, lr=0.01, min_delta=0.001)
            # Log training process
            training_log = nngls_model.train(data_train, data_val, data_test, Update_init=10, Update_step=10)
        elif model_name == "xgboost":
            raise NotImplementedError
        else:
            raise ValueError(f"Unknown model name: {model_name}")

    return hyperparams, model


def estimate_ci(model):
    """
    Estimate confidence intervals for the model
    using MapieRegressor
    Args:
        model:

    Returns:

    """
    from mapie.regression import MapieRegressor

    model = MapieRegressor(model, n_jobs=1)

    return model
