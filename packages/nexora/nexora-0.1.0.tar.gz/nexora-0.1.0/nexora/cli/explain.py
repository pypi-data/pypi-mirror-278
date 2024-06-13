import os
import pandas as pd
import json
import joblib
from argparse import ArgumentParser

from shapash import SmartExplainer
from . import BaseCommand


def explain_autotuna_command_factory(args):
    return ExplainAutoTunaCommand(
        args.model_path,
        args.data_path,
        args.config_path,
        args.features_path,
        args.port,
        args.host,
    )


class ExplainAutoTunaCommand(BaseCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        _parser = parser.add_parser("explain", help="Explain AutoTuna Models")
        _parser.add_argument(
            "--model_path", help="Path to model", required=True, type=str
        )
        _parser.add_argument(
            "--data_path", help="Path to data", required=True, type=str
        )
        _parser.add_argument(
            "--config_path", help="Path to config", required=True, type=str
        )
        _parser.add_argument(
            "--features_path", help="Path to features", required=True, type=str
        )
        _parser.add_argument(
            "--port", help="Port to serve on", default=8050, type=int, required=False
        )
        _parser.add_argument(
            "--host",
            help="Host to serve on",
            default="0.0.0.0",
            type=str,
            required=False,
        )
        _parser.set_defaults(func=explain_autotuna_command_factory)

    def __init__(self, model_path, data_path, config_path, features_path, port, host):
        self.model_path = model_path
        self.data_path = data_path
        self.config_path = config_path
        self.features_path = features_path
        self.port = port
        self.host = host

    def execute(self):
        os.environ["AUTOTUNA_MODEL_PATH"] = self.model_path
        model = joblib.load(self.model_path)
        config = joblib.load(self.config_path)
        df = pd.read_feather(self.data_path)
        with open(self.features_path) as f:
            features_dict = json.load(f)
        x = df[list(features_dict.keys())]
        y = df[config.targets]
        xpl = SmartExplainer(
            model=model,
            features_dict=features_dict,
            explainer_args={"algorithm": "tree"},
        )
        xpl.compile(x=x, y_target=y)
        _ = xpl.run_app(title_story=config.output, host=self.host, port=self.port)
