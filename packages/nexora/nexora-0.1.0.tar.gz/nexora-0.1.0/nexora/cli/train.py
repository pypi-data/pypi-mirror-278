from argparse import ArgumentParser

from ..autotuna import AutoTuna
from ..enums import TaskType
from . import BaseCommand


def train_autotuna_command_factory(args):
    return TrainAutoTunaCommand(
        args.algo,
        args.objective,
        args.fs,
        args.train_filename,
        args.idx,
        args.targets,
        args.task,
        args.output,
        args.features,
        args.num_folds,
        args.use_gpu,
        args.seed,
        args.test_filename,
        args.time_limit,
        args.fast,
        args.num_trials,
        args.categorical_features,
    )


class TrainAutoTunaCommand(BaseCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        _parser = parser.add_parser("train", help="Train a new model using AutoTuna")
        _parser.add_argument(
            "--algo",
            help="Algorithm Name",
            required=True,
            type=str,
        )
        _parser.add_argument(
            "--objective",
            help="Objective Name",
            required=False,
            type=str,
            default="loss",
        )
        _parser.add_argument("--fs", help="Feature Selection", type=int, default=0)
        _parser.add_argument(
            "--train_filename",
            help="Path to training file",
            required=True,
            type=str,
        )
        _parser.add_argument(
            "--test_filename",
            help="Path to test file",
            required=False,
            type=str,
            default=None,
        )
        _parser.add_argument(
            "--output",
            help="Path to output directory",
            required=True,
            type=str,
        )
        _parser.add_argument(
            "--task",
            help="User defined task type",
            required=False,
            type=str,
            default=None,
            choices=TaskType.list_str(),
        )
        _parser.add_argument(
            "--idx",
            help="ID column",
            required=False,
            type=str,
            default="id",
        )
        _parser.add_argument(
            "--targets",
            help="Target column(s). If there are multiple targets, separate by ';'",
            required=False,
            type=str,
            default="target",
        )
        _parser.add_argument(
            "--num_folds",
            help="Number of folds to use",
            required=False,
            type=int,
            default=5,
        )
        _parser.add_argument(
            "--num_trials",
            help="Number of trials to use",
            required=False,
            type=int,
            default=100,
        )
        _parser.add_argument(
            "--features",
            help="Features to use, separated by ';'",
            required=False,
            type=str,
            default=None,
        )
        _parser.add_argument(
            "--categorical_features",
            help="Categorical features to use, separated by ';'",
            required=False,
            type=str,
            default=None,
        )
        _parser.add_argument(
            "--use_gpu",
            help="Whether to use GPU for training",
            action="store_true",
            required=False,
        )
        _parser.add_argument(
            "--fast",
            help="Whether to use fast mode for tuning params. Only one fold will be used if fast mode is set",
            action="store_true",
            required=False,
        )
        _parser.add_argument(
            "--seed",
            help="Random seed",
            required=False,
            type=int,
            default=42,
        )
        _parser.add_argument(
            "--time_limit",
            help="Time limit for optimization",
            required=False,
            type=int,
            default=None,
        )

        _parser.set_defaults(func=train_autotuna_command_factory)

    def __init__(
        self,
        algo,
        objective,
        fs,
        train_filename,
        idx,
        targets,
        task,
        output,
        features,
        num_folds,
        use_gpu,
        seed,
        test_filename,
        time_limit,
        fast,
        num_trials,
        categorical_features,
    ):
        self.train_filename = train_filename
        self.idx = idx
        self.targets = targets.split(";")
        self.task = task
        self.output = output
        self.features = features.split(";") if features else None
        self.num_folds = num_folds
        self.use_gpu = use_gpu
        self.seed = seed
        self.test_filename = test_filename
        self.time_limit = time_limit
        self.fast = fast
        self.algo = algo
        self.objective = objective
        self.fs = fs
        self.num_trials = num_trials
        self.categorical_features = (
            categorical_features.split(";") if features else None
        )

    def execute(self):
        atuna = AutoTuna(
            train_filename=self.train_filename,
            idx=self.idx,
            targets=self.targets,
            task=self.task,
            output=self.output,
            features=self.features,
            num_folds=self.num_folds,
            use_gpu=self.use_gpu,
            seed=self.seed,
            test_filename=self.test_filename,
            time_limit=self.time_limit,
            fast=self.fast,
            algo=self.algo,
            objective=self.objective,
            fs=self.fs,
            num_trials=self.num_trials,
            categorical_features=self.categorical_features,
        )
        atuna.train()
