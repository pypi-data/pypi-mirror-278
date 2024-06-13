import copy
import os
from functools import partial
from typing import Any

import joblib
import numpy as np
import optuna
import pandas as pd
import xgboost as xgb
import lightgbm as lgbm
from sklearn.ensemble import RandomForestClassifier

from .enums import ProblemType, Algo, Objective
from .logger import logger
from .metrics import Metrics
from .params import get_params
from .boruta import BorutaPy
from .schemas import ModelConfig


optuna.logging.set_verbosity(optuna.logging.INFO)


def reduce_memory_usage(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Shrinking the given data frame's memory usage by tuning data types.

    Args:
        df (pd.DataFrame): Input data frame.
        verbose (bool): Verbose option. Defaults to True.

    Returns:
        pd.DataFrame: Output data frame.
    """
    # NOTE: Original author of this function is unknown
    # if you know the *original author*, please let me know.
    numerics = ["int8", "int16", "int32", "int64", "float16", "float32", "float64"]
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == "int":
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if (
                    c_min > np.finfo(np.float16).min
                    and c_max < np.finfo(np.float16).max
                ):
                    df[col] = df[col].astype(np.float16)
                elif (
                    c_min > np.finfo(np.float32).min
                    and c_max < np.finfo(np.float32).max
                ):
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose:
        logger.info(
            "Mem. usage decreased to {:.2f} Mb ({:.1f}% reduction)".format(
                end_mem, 100 * (start_mem - end_mem) / start_mem
            )
        )
    return df


def dict_mean(dict_list: list) -> dict:
    """
    Average of the given list of dictionary.

    Args:
        list: Input data, list of dictionary

    Returns:
        dict: Output data
    """
    mean_dict = {}
    for key in dict_list[0].keys():
        mean_dict[key] = sum(d[key] for d in dict_list) / len(dict_list)
    return mean_dict


def save_valid_predictions(
    final_valid_predictions: list,
    model_config: ModelConfig,
    target_encoder: Any,
    output_file_name: str,
) -> None:
    """
    Persist final validation predictions to csv

    Args:
        final_valid_predictions (list): Final Predictions list
        model_config (ModelConfig): Model Configuration
        target_encoder (Any): Target Encoder Model, TODO: Clarify the variable type
        output_file_name (str): Output file name

    Returns:
        None
    """
    final_valid_predictions = pd.DataFrame.from_dict(
        final_valid_predictions, orient="index"
    ).reset_index()
    if target_encoder is None:
        final_valid_predictions.columns = [model_config.idx] + model_config.targets
    else:
        final_valid_predictions.columns = [model_config.idx] + list(
            target_encoder.classes_
        )

    final_valid_predictions.to_csv(
        os.path.join(model_config.output, output_file_name),
        index=False,
    )


def save_test_predictions(
    final_test_predictions: dict,
    model_config: ModelConfig,
    target_encoder: Any,
    test_ids: np.ndarray,
    output_file_name: str,
) -> None:
    """
    Persist final test predictions to csv

    Args:
        final_valid_predictions (list): Final Predictions list
        model_config (ModelConfig): Model Configuration
        target_encoder (Any): Target Encoder Model, TODO: Clarify the variable type
        test_ids (np.ndarray): Test data ID values
        output_file_name (str): Output file name

    Returns:
        None
    """
    final_test_predictions = np.mean(final_test_predictions, axis=0)
    if target_encoder is None:
        final_test_predictions = pd.DataFrame(
            final_test_predictions, columns=model_config.targets
        )
    else:
        final_test_predictions = pd.DataFrame(
            final_test_predictions, columns=list(target_encoder.classes_)
        )
    final_test_predictions.insert(loc=0, column=model_config.idx, value=test_ids)
    final_test_predictions.to_csv(
        os.path.join(model_config.output, output_file_name),
        index=False,
    )


def fetch_model_params(model_config: ModelConfig) -> tuple:
    """
    Fetching model parameters

    Args:
        model_config (ModelConfig): Model Configuration

    Returns:
        tuple: tree_model, use_predict_proba, eval_metric, direction
    """
    if model_config.problem_type == ProblemType.binary_classification:
        if model_config.objective == Objective.loss.value:
            if model_config.algo == Algo.xgb.value:
                tree_model = xgb.XGBClassifier
                eval_metric = "logloss"
            elif model_config.algo == Algo.lgbm.value:
                tree_model = lgbm.LGBMClassifier
                eval_metric = "binary_logloss"
            else:
                raise NotImplementedError
            use_predict_proba = True
            direction = "minimize"
        elif model_config.objective == Objective.accuracy.value:
            if model_config.algo == Algo.xgb.value:
                tree_model = xgb.XGBClassifier
                eval_metric = "accuracy"
            elif model_config.algo == Algo.lgbm.value:
                tree_model = lgbm.LGBMClassifier
                eval_metric = "accuracy"
            else:
                raise NotImplementedError
            direction = "maximize"
        else:
            raise NotImplementedError
    elif model_config.problem_type == ProblemType.multi_class_classification:
        if model_config.objective == Objective.loss.value:
            if model_config.algo == Algo.xgb.value:
                tree_model = xgb.XGBClassifier
                eval_metric = "mlogloss"
            elif model_config.algo == Algo.lgbm.value:
                tree_model = lgbm.LGBMClassifier
                eval_metric = "multi_logloss"
            else:
                raise NotImplementedError
            use_predict_proba = True
            direction = "minimize"
        elif model_config.objective == Objective.accuracy.value:
            if model_config.algo == Algo.xgb.value:
                tree_model = xgb.XGBClassifier
                eval_metric = "accuracy"
            elif model_config.algo == Algo.lgbm.value:
                tree_model = lgbm.LGBMClassifier
                eval_metric = "accuracy"
            else:
                raise NotImplementedError
            direction = "maximize"
        else:
            raise NotImplementedError
    elif model_config.problem_type == ProblemType.multi_label_classification:
        if model_config.objective == Objective.loss.value:
            if model_config.algo == Algo.xgb.value:
                tree_model = xgb.XGBClassifier
                eval_metric = "logloss"
            elif model_config.algo == Algo.lgbm.value:
                tree_model = lgbm.LGBMClassifier
                eval_metric = "binary_logloss"
            else:
                raise NotImplementedError
            use_predict_proba = True
            direction = "minimize"
        elif model_config.objective == Objective.accuracy.value:
            if model_config.algo == Algo.xgb.value:
                tree_model = xgb.XGBClassifier
                eval_metric = "accuracy"
            elif model_config.algo == Algo.lgbm.value:
                tree_model = lgbm.LGBMClassifier
                eval_metric = "accuracy"
            else:
                raise NotImplementedError
            use_predict_proba = True
            direction = "maximize"
        else:
            raise NotImplementedError
    elif model_config.problem_type == ProblemType.single_column_regression:
        if model_config.algo == Algo.xgb.value:
            tree_model = xgb.XGBRegressor
        elif model_config.algo == Algo.lgbm.value:
            tree_model = lgbm.LGBMRegressor
        else:
            raise NotImplementedError
        eval_metric = "rmse"
        use_predict_proba = False
        direction = "minimize"
    elif model_config.problem_type == ProblemType.multi_column_regression:
        if model_config.algo == Algo.xgb.value:
            tree_model = xgb.XGBRegressor
        elif model_config.algo == Algo.lgbm.value:
            tree_model = lgbm.LGBMRegressor
        else:
            raise NotImplementedError
        eval_metric = "rmse"
        use_predict_proba = False
        direction = "minimize"
    else:
        raise NotImplementedError

    return tree_model, use_predict_proba, eval_metric, direction


def optimize(
    trial: optuna.Trial,
    tree_model: Any,
    use_predict_proba: bool,
    eval_metric: str,
    model_config: ModelConfig,
) -> float:
    """
    Optimization function

    Args:
        trial (optuna.Trial): Trial
        tree_model (Any): Tree Model object incl xgb, lgbm
        use_predict_proba (bool): Likelihood probabilities
        eval_metric (str): Metric name
        model_config (ModelConfig): Model configuration

    Returns:
        float: Metric value
    """
    params = get_params(trial, model_config)
    early_stopping_rounds = params["early_stopping_rounds"]
    del params["early_stopping_rounds"]

    metrics = Metrics(model_config.problem_type, model_config.algo)

    scores = []

    for fold in range(model_config.num_folds):
        train_feather = pd.read_feather(
            os.path.join(model_config.output, f"train_fold_{fold}.feather")
        )
        valid_feather = pd.read_feather(
            os.path.join(model_config.output, f"valid_fold_{fold}.feather")
        )
        xtrain = train_feather[model_config.features]
        xvalid = valid_feather[model_config.features]

        ytrain = train_feather[model_config.targets].values
        yvalid = valid_feather[model_config.targets].values

        # train model
        model = tree_model(
            random_state=model_config.seed,
            eval_metric=eval_metric,
            use_label_encoder=False,
            **params,
        )

        if model_config.problem_type in (
            ProblemType.multi_column_regression,
            ProblemType.multi_label_classification,
        ):
            ypred = []
            models = [model] * len(model_config.targets)
            for idx, _m in enumerate(models):
                _m.fit(
                    xtrain,
                    ytrain[:, idx],
                    early_stopping_rounds=early_stopping_rounds,
                    eval_set=[(xvalid, yvalid[:, idx])],
                    verbose=False,
                )
                if model_config.problem_type == ProblemType.multi_column_regression:
                    ypred_temp = _m.predict(xvalid)
                else:
                    ypred_temp = _m.predict_proba(xvalid)[:, 1]
                ypred.append(ypred_temp)
            ypred = np.column_stack(ypred)

        else:
            model.fit(
                xtrain,
                ytrain,
                early_stopping_rounds=early_stopping_rounds,
                eval_set=[(xvalid, yvalid)],
                verbose=False,
            )

            if use_predict_proba:
                ypred = model.predict_proba(xvalid)
            else:
                ypred = model.predict(xvalid)

        # calculate metric
        metric_dict = metrics.calculate(yvalid, ypred)
        scores.append(metric_dict)
        if model_config.fast is True:
            break

    mean_metrics = dict_mean(scores)
    logger.info(f"Metrics: {mean_metrics}")
    return mean_metrics[eval_metric]


def train_model(model_config: ModelConfig) -> dict:
    """
    Train model

    Args:
        model_config (ModelConfig): Model configuration

    Returns:
        dict: Best params
    """
    tree_model, use_predict_proba, eval_metric, direction = fetch_model_params(
        model_config
    )

    optimize_func = partial(
        optimize,
        tree_model=tree_model,
        use_predict_proba=use_predict_proba,
        eval_metric=eval_metric,
        model_config=model_config,
    )
    db_path = os.path.join(model_config.output, "params.db")
    study = optuna.create_study(
        direction=direction,
        study_name="autotuna",
        storage=f"sqlite:///{db_path}",
        load_if_exists=True,
    )

    logger.info("======================================================")
    logger.info("|                                                    |")
    logger.info("|                                                    |")
    logger.info("|  Monitor the study                                 |")
    logger.info("| Run the following command under the output folder: |")
    logger.info(f"| cd  {db_path}                                     |")
    logger.info("| optuna-dashboard sqlite:///params.db               |")
    logger.info("|                                                    |")
    logger.info("|                                                    |")
    logger.info("======================================================")

    study.optimize(
        optimize_func, n_trials=model_config.num_trials, timeout=model_config.time_limit
    )
    return study.best_params


def predict_model(model_config: ModelConfig, best_params: dict) -> None:
    """
    Predict model

    Args:
        model_config (ModelConfig): Model configuration
        best_params (dict): Best parameters

    Returns:
        None
    """
    early_stopping_rounds = best_params["early_stopping_rounds"]
    del best_params["early_stopping_rounds"]

    if model_config.use_gpu is True:
        best_params["tree_method"] = "gpu_hist"
        best_params["gpu_id"] = 0
        best_params["predictor"] = "gpu_predictor"

    tree_model, use_predict_proba, eval_metric, _ = fetch_model_params(model_config)

    metrics = Metrics(model_config.problem_type, model_config.algo)
    scores = []

    final_test_predictions = []
    final_valid_predictions = {}

    target_encoder = joblib.load(f"{model_config.output}/atuna.target_encoder")

    for fold in range(model_config.num_folds):
        logger.info(f"Training and predicting for fold {fold}")
        train_feather = pd.read_feather(
            os.path.join(model_config.output, f"train_fold_{fold}.feather")
        )
        valid_feather = pd.read_feather(
            os.path.join(model_config.output, f"valid_fold_{fold}.feather")
        )

        xtrain = train_feather[model_config.features]
        xvalid = valid_feather[model_config.features]

        valid_ids = valid_feather[model_config.idx].values

        if model_config.test_filename is not None:
            test_feather = pd.read_feather(
                os.path.join(model_config.output, f"test_fold_{fold}.feather")
            )
            xtest = test_feather[model_config.features]
            test_ids = test_feather[model_config.idx].values

        ytrain = train_feather[model_config.targets].values
        yvalid = valid_feather[model_config.targets].values

        model = tree_model(
            random_state=model_config.seed,
            eval_metric=eval_metric,
            use_label_encoder=False,
            **best_params,
        )

        if model_config.problem_type in (
            ProblemType.multi_column_regression,
            ProblemType.multi_label_classification,
        ):
            ypred = []
            test_pred = []
            trained_models = []
            for idx in range(len(model_config.targets)):
                _m = copy.deepcopy(model)
                _m.fit(
                    xtrain,
                    ytrain[:, idx],
                    early_stopping_rounds=early_stopping_rounds,
                    eval_set=[(xvalid, yvalid[:, idx])],
                    verbose=False,
                )
                trained_models.append(_m)
                if model_config.problem_type == ProblemType.multi_column_regression:
                    ypred_temp = _m.predict(xvalid)
                    if model_config.test_filename is not None:
                        test_pred_temp = _m.predict(xtest)
                else:
                    ypred_temp = _m.predict_proba(xvalid)[:, 1]
                    if model_config.test_filename is not None:
                        test_pred_temp = _m.predict_proba(xtest)[:, 1]

                ypred.append(ypred_temp)
                if model_config.test_filename is not None:
                    test_pred.append(test_pred_temp)

            ypred = np.column_stack(ypred)
            if model_config.test_filename is not None:
                test_pred = np.column_stack(test_pred)
            joblib.dump(
                trained_models,
                os.path.join(
                    model_config.output,
                    f"atuna_model.{fold}",
                ),
            )

        else:
            model.fit(
                xtrain,
                ytrain,
                early_stopping_rounds=early_stopping_rounds,
                eval_set=[(xvalid, yvalid)],
                verbose=False,
            )

            joblib.dump(
                model,
                os.path.join(
                    model_config.output,
                    f"atuna_model.{fold}",
                ),
            )

            if use_predict_proba:
                ypred = model.predict_proba(xvalid)
                if model_config.test_filename is not None:
                    test_pred = model.predict_proba(xtest)
            else:
                ypred = model.predict(xvalid)
                if model_config.test_filename is not None:
                    test_pred = model.predict(xtest)

        final_valid_predictions.update(dict(zip(valid_ids, ypred)))
        if model_config.test_filename is not None:
            final_test_predictions.append(test_pred)

        # calculate metric
        metric_dict = metrics.calculate(yvalid, ypred)
        scores.append(metric_dict)
        logger.info(f"Fold {fold} done!")

    mean_metrics = dict_mean(scores)
    logger.info(f"Metrics: {mean_metrics}")
    save_valid_predictions(
        final_valid_predictions, model_config, target_encoder, "oof_predictions.csv"
    )

    if model_config.test_filename is not None:
        save_test_predictions(
            final_test_predictions,
            model_config,
            target_encoder,
            test_ids,
            "test_predictions.csv",
        )
    else:
        logger.info("No test data supplied. Only OOF predictions were generated")


def select_features(model_config: ModelConfig, fold: int = 0, seed: int = 0) -> list:
    """
    Feature selection

    Args:
        model_config (ModelConfig): Model configuration
        fold (int): Fold number. Defaults to 0
        seed (int): Seed number. Defaults to 0

    Returns:
        list: Selected features
    """

    train_feather = pd.read_feather(
        os.path.join(model_config.output, f"train_fold_{fold}.feather")
    )
    valid_feather = pd.read_feather(
        os.path.join(model_config.output, f"valid_fold_{fold}.feather")
    )

    x = pd.concat(
        [train_feather[model_config.features], valid_feather[model_config.features]]
    )
    y = pd.concat(
        [train_feather[model_config.targets], valid_feather[model_config.targets]]
    )
    if model_config.problem_type in [
        ProblemType.binary_classification,
        ProblemType.multi_class_classification,
    ]:
        model = RandomForestClassifier(
            n_jobs=-1, class_weight=None, max_depth=7, random_state=seed
        )
    elif model_config.problem_type in [ProblemType.multi_column_regression]:
        model = xgb.XGBRegressor(seed=seed)
    else:
        raise NotImplementedError

    feat_selector = BorutaPy(model, n_estimators="auto", verbose=2, random_state=seed)
    feat_selector.fit(x.values, y.values)
    selected_features = x.columns[feat_selector.support_]
    joblib.dump(
        feat_selector, os.path.join(model_config.output, "atuna.feature_selection")
    )
    # selected = x.values[:, feat_selector.support_]
    logger.info("Feature selection is done, selected features:")
    logger.info(selected_features)
    return selected_features
