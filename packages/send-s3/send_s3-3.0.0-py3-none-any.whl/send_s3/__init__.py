import sys
import argparse

from send_s3.common import PROG, VERSION
from send_s3.actions import ACTIONS


def main() -> None:
    parser = argparse.ArgumentParser(prog=PROG)
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    subparsers = parser.add_subparsers(dest='action', required=True)
    for action_name, module in ACTIONS.items():
        subparser = subparsers.add_parser(action_name)
        module.register_arguments(subparser)
    args = parser.parse_args()
    sys.exit(ACTIONS[args.action].main(args))


__all__ = ['main']
