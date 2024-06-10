import argparse

import requests

from ambientctl.config import settings


def get_parser():
    parser = argparse.ArgumentParser(
        prog="auth",
        usage="ambientctl %(prog)s [options]",
        description="Manage authorization actions.",
        epilog="Example: ambientctl auth --node-id <node_id> \
--device-code <device_code>",
        add_help=False,  # Suppress the default help argument
    )
    parser.add_argument("-n", "--node-id", help="Node ID")
    parser.add_argument("-d", "--device-code", help="Device code")

    # Subcommands
    # subparsers = parser.add_subparsers()
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to run")

    # Subparser for the 'status' command
    status_parser = subparsers.add_parser(  # noqa
        "status", help="Check authorization status"
    )

    return parser


def check_status():
    url = f"{settings.ambient_server}/auth/status"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(response.json()["status"])
    except Exception as e:
        print(f"error: {e}")
        return


def authorize_node(node_id: str, device_code: str):
    url = f"{settings.ambient_server}/auth?node_id={node_id}&device_code={device_code}"
    try:
        response = requests.post(url)
        response.raise_for_status()
        print(response.json())
    except Exception as e:
        print(f"error: {e}")
        return


def run(args):
    # print("args: ", args)
    if args.command == "status":
        check_status()
        return

    if args.node_id and args.device_code:
        authorize_node(args.node_id, args.device_code)
        return
