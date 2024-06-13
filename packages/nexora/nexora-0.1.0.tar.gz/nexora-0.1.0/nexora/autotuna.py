import os
import json
from dataclasses import dataclass
from typing import List, Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.utils.multiclass import type_of_target

from .enums import ProblemType
from .logger import logger
from .schemas import ModelConfig
from .utils import predict_model, reduce_memory_usage, train_model, select_features


@dataclass
class AutoTuna:
    """
    AutoTuna is the entrypoint class derived from dataclass

    The constructor allows the following arguments and run training and prediction methods.

    Args:
        train_file_name (str): Training data location.
        output (str): Output directory location. Fails if already exists.
        algo (str): ML algorithm for trainig including xgb, lgbm
        objective (str, optional): Objective function to optimize with optuna. Defaults to 'loss'.
        test_filename (str, optional): Test data location to evaluate the model. Defaults to None.
        task (str, optional): ML task type either classification or regression. Defaults to None.
        idx (str, optional): Unique identifier column in the data which helps sampling and splitting. Defaults to 'id'.
        targets (List[str], optional): Target column names. Defaults to None.
        features (List[str], optional): Selected feature names. Defaults to None.
        categorical_features (List[str], optional): Categorigal feature names. Defaults to None.
        use_gpu (bool, optional): Utilise gpu devices if applicable. Defaults to False.
        num_folds (int, optional): Number of folds for cross-validation. Defaults to 5.
        seed (int, optional): Seed number for random sampling and model build. Defaults to 42.
        num_trials (int, optional): The number of study for optimization. Defaults to 1000.
        time_limit (int, optional): Time limit for optimization. Defaults to None.
        fast (bool, optional): Fast mode for tuning params. Only one fold will be used if fast mode is set. Defaults to False.
        fs (int, optional): Feature selection with boruta. Defaults to 0.

    """

    # required arguments
    train_filename: str
    output: str
    algo: str

    objective: Optional[str] = "loss"
    # optional arguments
    test_filename: Optional[str] = None
    task: Optional[str] = None
    idx: Optional[str] = "id"
    targets: Optional[List[str]] = None
    features: Optional[List[str]] = None
    categorical_features: Optional[List[str]] = None
    use_gpu: Optional[bool] = False
    num_folds: Optional[int] = 5
    seed: Optional[int] = 42
    num_trials: Optional[int] = 1000
    time_limit: Optional[int] = None
    fast: Optional[bool] = False
    fs: Optional[int] = 0

    def __post_init__(self):
        if os.path.exists(self.output):
            raise Exception(
                "Output directory already exists. Please specify some other directory."
            )
        os.makedirs(self.output, exist_ok=True)
        logger.info(f"Output directory: {self.output}")

        if self.targets is None:
            logger.warning("No target columns specified. Will default to `target`.")
            self.targets = ["target"]

        if self.idx is None:
            logger.warning("No id column specified. Will default to `id`.")
            self.idx = "id"

    def _create_folds(
        self, train_df: pd.DataFrame, problem_type: ProblemType
    ) -> pd.DataFrame:
        """
        Create k-folds for cross validation

        Args:
            train_df (pd.DataFrame): Input Data Frame

        Returns:
            pd.DataFrame: Output data frame
        """
        if "kfold" in train_df.columns:
            self.num_folds = len(np.unique(train_df["kfold"]))
            logger.info("Using `kfold` for folds from training data")
            return train_df

        logger.info("Creating folds")
        train_df["kfold"] = -1
        if problem_type in (
            ProblemType.binary_classification,
            ProblemType.multi_class_classification,
        ):
            y = train_df[self.targets].values
            kf = StratifiedKFold(
                n_splits=self.num_folds, shuffle=True, random_state=self.seed
            )
            for fold, (_, valid_indicies) in enumerate(kf.split(X=train_df, y=y)):
                train_df.loc[valid_indicies, "kfold"] = fold
        elif problem_type == ProblemType.single_column_regression:
            y = train_df[self.targets].values
            num_bins = int(np.floor(1 + np.log2(len(train_df))))
            if num_bins > 10:
                num_bins = 10
            kf = StratifiedKFold(
                n_splits=self.num_folds, shuffle=True, random_state=self.seed
            )
            train_df["bins"] = pd.cut(
                train_df[self.targets].values.ravel(), bins=num_bins, labels=False
            )
            for fold, (_, valid_indicies) in enumerate(
                kf.split(X=train_df, y=train_df.bins.values)
            ):
                train_df.loc[valid_indicies, "kfold"] = fold
            train_df = train_df.drop("bins", axis=1)
        elif problem_type == ProblemType.multi_column_regression:
            y = train_df[self.targets].values
            kf = KFold(n_splits=self.num_folds, shuffle=True, random_state=self.seed)
            for fold, (_, valid_indicies) in enumerate(kf.split(X=train_df, y=y)):
                train_df.loc[valid_indicies, "kfold"] = fold
        # TODO: use iterstrat
        elif problem_type == ProblemType.multi_label_classification:
            y = train_df[self.targets].values
            kf = KFold(n_splits=self.num_folds, shuffle=True, random_state=self.seed)
            for fold, (_, valid_indicies) in enumerate(kf.split(X=train_df, y=y)):
                train_df.loc[valid_indicies, "kfold"] = fold
        else:
            raise Exception("Problem type not supported")
        return train_df

    def _determine_problem_type(self, train_df: pd.DataFrame) -> ProblemType:
        """
        Identify problem type for the given data frame.

        Args:
            train_df (pd.DataFrame): Input Data Frame

        Returns:
            ProblemType: ML Problem
        """
        if self.task is not None:
            if self.task == "classification":
                if len(self.targets) == 1:
                    if len(np.unique(train_df[self.targets].values)) == 2:
                        problem_type = ProblemType.binary_classification
                    else:
                        problem_type = ProblemType.multi_class_classification
                else:
                    problem_type = ProblemType.multi_label_classification

            elif self.task == "regression":
                if len(self.targets) == 1:
                    problem_type = ProblemType.single_column_regression
                else:
                    problem_type = ProblemType.multi_column_regression
            else:
                raise Exception("Problem type not understood")

        else:
            target_type = type_of_target(train_df[self.targets].values)
            # target type is one of the following using scikit-learn's type_of_target
            # * 'continuous': `y` is an array-like of floats that are not all
            #   integers, and is 1d or a column vector.
            # * 'continuous-multioutput': `y` is a 2d array of floats that are
            #   not all integers, and both dimensions are of size > 1.
            # * 'binary': `y` contains <= 2 discrete values and is 1d or a column
            #   vector.
            # * 'multiclass': `y` contains more than two discrete values, is not a
            #   sequence of sequences, and is 1d or a column vector.
            # * 'multiclass-multioutput': `y` is a 2d array that contains more
            #   than two discrete values, is not a sequence of sequences, and both
            #   dimensions are of size > 1.
            # * 'multilabel-indicator': `y` is a label indicator matrix, an array
            #   of two dimensions with at least two columns, and at most 2 unique
            #   values.
            # * 'unknown': `y` is array-like but none of the above, such as a 3d
            #   array, sequence of sequences, or an array of non-sequence objects.
            if target_type == "continuous":
                problem_type = ProblemType.single_column_regression
            elif target_type == "continuous-multioutput":
                problem_type = ProblemType.multi_column_regression
            elif target_type == "binary":
                problem_type = ProblemType.binary_classification
            elif target_type == "multiclass":
                problem_type = ProblemType.multi_class_classification
            elif target_type == "multilabel-indicator":
                problem_type = ProblemType.multi_label_classification
            else:
                raise Exception(
                    "Unable to infer `problem_type`. Please provide `classification` or `regression`"
                )
        logger.info(f"Problem type: {problem_type.name}")
        return problem_type

    def _inject_idxumn(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Injecting ID column to the given data framework

        Args:
            df (pd.DataFrame): Input Data Frame

        Returns:
            pd.DataFrame: Output Data Frame along with ID column
        """
        if self.idx not in df.columns:
            df[self.idx] = np.arange(len(df))
        return df

    def _process_data(self) -> None:
        """
        Data pre-processing

        Returns:
            None
        """
        logger.info("Reading training data")
        train_df = pd.read_csv(self.train_filename)
        train_df = reduce_memory_usage(train_df)
        problem_type = self._determine_problem_type(train_df)

        train_df = self._inject_idxumn(train_df)
        if self.test_filename is not None:
            test_df = pd.read_csv(self.test_filename)
            test_df = reduce_memory_usage(test_df)
            test_df = self._inject_idxumn(test_df)

        # create folds
        train_df = self._create_folds(train_df, problem_type)
        ignore_columns = [self.idx, "kfold"] + self.targets

        if self.features is None:
            self.features = list(train_df.columns)
            self.features = [x for x in self.features if x not in ignore_columns]

        # encode target(s)
        if problem_type in [
            ProblemType.binary_classification,
            ProblemType.multi_class_classification,
        ]:
            logger.info("Encoding target(s)")
            target_encoder = LabelEncoder()
            target_encoder.fit(
                train_df[self.targets].values.reshape(
                    -1,
                )
            )
            train_df.loc[:, self.targets] = target_encoder.transform(
                train_df[self.targets].values.reshape(
                    -1,
                )
            )
        else:
            target_encoder = None

        if self.categorical_features is None:
            # find categorical features
            categorical_features = []
            for col in self.features:
                if train_df[col].dtype == "object":
                    categorical_features.append(col)

        else:
            categorical_features = self.categorical_features

        logger.info(f"Found {len(categorical_features)} categorical features.")

        if len(categorical_features) > 0:
            logger.info("Encoding categorical features")
        categorical_encoders = {}
        for fold in range(self.num_folds):
            fold_train = train_df[train_df.kfold != fold].reset_index(drop=True)
            fold_valid = train_df[train_df.kfold == fold].reset_index(drop=True)
            if self.test_filename is not None:
                test_fold = test_df.copy(deep=True)
            if len(categorical_features) > 0:
                ord_encoder = OrdinalEncoder(
                    handle_unknown="use_encoded_value", unknown_value=np.nan
                )
                fold_train[categorical_features] = ord_encoder.fit_transform(
                    fold_train[categorical_features].values
                )
                fold_valid[categorical_features] = ord_encoder.transform(
                    fold_valid[categorical_features].values
                )
                if self.test_filename is not None:
                    test_fold[categorical_features] = ord_encoder.transform(
                        test_fold[categorical_features].values
                    )
                categorical_encoders[fold] = ord_encoder
            fold_train.to_feather(
                os.path.join(self.output, f"train_fold_{fold}.feather")
            )
            fold_valid.to_feather(
                os.path.join(self.output, f"valid_fold_{fold}.feather")
            )
            if self.test_filename is not None:
                test_fold.to_feather(
                    os.path.join(self.output, f"test_fold_{fold}.feather")
                )

        # save config
        model_config = {}
        model_config["idx"] = self.idx
        model_config["features"] = self.features
        model_config["categorical_features"] = categorical_features
        model_config["train_filename"] = self.train_filename
        model_config["test_filename"] = self.test_filename
        model_config["output"] = self.output
        model_config["problem_type"] = problem_type
        model_config["idx"] = self.idx
        model_config["targets"] = self.targets
        model_config["use_gpu"] = self.use_gpu
        model_config["num_folds"] = self.num_folds
        model_config["seed"] = self.seed
        model_config["num_trials"] = self.num_trials
        model_config["time_limit"] = self.time_limit
        model_config["fast"] = self.fast
        model_config["algo"] = self.algo
        model_config["fs"] = self.fs
        model_config["objective"] = self.objective

        self.model_config = ModelConfig(**model_config)
        logger.info(f"Model config: {self.model_config}")
        logger.info("Saving model config")
        joblib.dump(self.model_config, f"{self.output}/atuna.config")

        # save encoders
        logger.info("Saving encoders")
        joblib.dump(categorical_encoders, f"{self.output}/atuna.categorical_encoders")
        joblib.dump(target_encoder, f"{self.output}/atuna.target_encoder")

    def train(self) -> None:
        """
        Model training method.
        1) Preprocess data: Shrinking data types to reduce memory usage.
        2) Preprocess data: Determine the problem type
        3) Preprocess data: Inject idx column if requried
        4) Preprocess data: apply preprocessing to test data if applicable
        5) Preprocess data: Create folds for cross-validation
        6) Preprocess data: Apply target encoding if applicable
        7) Preprocess data: Apply categorical feature encoding
        8) If feature selection was enabled in the config then call the boruta feature selection method
        9) Update the features prop in the model config with the selected features if applicable.
        10) Train model with the given model config and find the best parameters after optimization.
        11) Save the best parameters under the workspace as a json file in order to re-use later and debug it.
        12) save selected features as a json file under the workspace
        13) Call the prediction method for OOF and test predictions.

        Returns:
            None
        """
        self._process_data()

        if self.model_config.fs == 1:
            logger.info("Feature Importance Step")
            selected_features = select_features(self.model_config)
            self.model_config.features = selected_features
            logger.info("Features updated with selected features")
            logger.info(selected_features)

        best_params = train_model(self.model_config)

        logger.info(f"Best params: {best_params}")
        with open(os.path.join(self.model_config.output, "best_params.json"), "w") as f:
            json.dump(best_params, f)

        selected_features_dict = {f: f for f in self.model_config.features}
        with open(
            os.path.join(self.model_config.output, "selected_features.json"), "w"
        ) as f:
            json.dump(selected_features_dict, f)

        logger.info("Training complete")
        self.predict(best_params)

    def predict(self, best_params: dict) -> None:
        """
        Predict the out-of-fold data with the current model and create the test predictions

        Args:
            best_params (dict): Best parameters after optimization.

        Returns:
            None
        """
        logger.info("Creating OOF and test predictions")
        predict_model(self.model_config, best_params)
