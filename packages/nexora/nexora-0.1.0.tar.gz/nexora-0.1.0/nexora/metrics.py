from dataclasses import dataclass
from functools import partial

import numpy as np
from sklearn import metrics as skmetrics

from .enums import ProblemType, Algo
import copy


@dataclass
class Metrics:
    """
    Metrics is derived from dataclass and assigns the problem_type, algorithm and metric types against them.

    Args:
        problem_type (ProblemType): Problem type enum.
        algo (Algo): Algorithm type enum.

    """

    problem_type: ProblemType
    algo: Algo

    def __post_init__(self) -> None:
        if self.problem_type == ProblemType.binary_classification:
            log_loss_key = "logloss"
            if self.algo == Algo.lgbm.value:
                log_loss_key = "binary_logloss"
            self.valid_metrics = {
                "auc": skmetrics.roc_auc_score,
                log_loss_key: skmetrics.log_loss,
                "f1": skmetrics.f1_score,
                "accuracy": skmetrics.accuracy_score,
                "precision": skmetrics.precision_score,
                "recall": skmetrics.recall_score,
            }
        elif self.problem_type == ProblemType.multi_class_classification:
            log_loss_key = "mlogloss"
            if self.algo == Algo.lgbm.value:
                log_loss_key = "multi_logloss"
            self.valid_metrics = {
                log_loss_key: skmetrics.log_loss,
                "accuracy": skmetrics.accuracy_score,
                "mlogloss": skmetrics.log_loss,
            }
        elif self.problem_type in (
            ProblemType.single_column_regression,
            ProblemType.multi_column_regression,
        ):
            self.valid_metrics = {
                "r2": skmetrics.r2_score,
                "mse": skmetrics.mean_squared_error,
                "mae": skmetrics.mean_absolute_error,
                "rmse": partial(skmetrics.mean_squared_error, squared=False),
                "rmsle": partial(skmetrics.mean_squared_log_error, squared=False),
            }
        elif self.problem_type == ProblemType.multi_label_classification:
            log_loss_key = "logloss"
            if self.algo == Algo.lgbm.value:
                log_loss_key = "binary_logloss"
            self.valid_metrics = {
                log_loss_key: skmetrics.log_loss,
            }
        else:
            raise Exception("Invalid problem type")

    def calculate(self, y_true: np.ndarray, y_pred: np.ndarray) -> dict:
        """
        Calculating the metrics

        Args:
            y_true (np.ndarray): Actual cases
            y_pred (np.ndarray): Predictions

        Returns:
            dict: Metrics dictionary
        """
        metrics = {}
        for metric_name, metric_func in self.valid_metrics.items():
            if self.problem_type == ProblemType.binary_classification:
                if metric_name == "auc":
                    metrics[metric_name] = metric_func(y_true, y_pred[:, 1])
                elif metric_name in ["logloss", "binary_logloss"]:
                    metrics[metric_name] = metric_func(y_true, y_pred)
                else:
                    metrics[metric_name] = metric_func(y_true, y_pred[:, 1] >= 0.5)
            elif self.problem_type == ProblemType.multi_class_classification:
                if metric_name == "accuracy":
                    metrics[metric_name] = metric_func(
                        y_true, np.argmax(y_pred, axis=1)
                    )
                else:
                    metrics[metric_name] = metric_func(y_true, y_pred)
            else:
                if metric_name == "rmsle":
                    temp_pred = copy.deepcopy(y_pred)
                    temp_pred[temp_pred < 0] = 0
                    metrics[metric_name] = metric_func(y_true, temp_pred)
                else:
                    metrics[metric_name] = metric_func(y_true, y_pred)
        return metrics
