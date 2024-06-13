import argparse

from .. import __version__

from .predict import PredictAutoTunaCommand
from .serve import ServeAutoTunaCommand
from .train import TrainAutoTunaCommand
from .explain import ExplainAutoTunaCommand
from .monitor import MonitorAutoTunaCommand


def main():
    parser = argparse.ArgumentParser(
        "AutoTuna CLI",
        usage="nexora <command> [<args>]",
        epilog="For more information about a command, run: `nexora <command> --help`",
    )
    parser.add_argument(
        "--version", "-v", help="Display AutoTuna version", action="store_true"
    )

    commands_parser = parser.add_subparsers(help="commands")
    TrainAutoTunaCommand.register_subcommand(commands_parser)
    PredictAutoTunaCommand.register_subcommand(commands_parser)
    ServeAutoTunaCommand.register_subcommand(commands_parser)
    ExplainAutoTunaCommand.register_subcommand(commands_parser)
    MonitorAutoTunaCommand.register_subcommand(commands_parser)

    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit(0)

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    command = args.func(args)
    command.execute()


if __name__ == "__main__":
    main()
