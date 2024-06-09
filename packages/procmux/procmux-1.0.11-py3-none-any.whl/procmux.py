
from app.__main__ import run_app
from app.args import cli_args
from app.config import parse_config


def start_cli():
    config = parse_config(cli_args.config, cli_args.config_override)
    run_app(config)

def send_signal():
    pass


if __name__ == '__main__':
    subcommand = cli_args.subcommand
