#!/usr/bin/env python3
from __future__ import annotations

import json as json_mod
import logging
import os
import subprocess
import sys
from functools import lru_cache
from typing import Any

import click
from tabulate import tabulate
from toolforge_weld.config import Config
from toolforge_weld.errors import ToolforgeError, ToolforgeUserError, print_error_context

from toolforge_envvars_cli.config import get_loaded_config
from toolforge_envvars_cli.envvars import EnvvarsClient

LOGGER = logging.getLogger("toolforge" if __name__ == "__main__" else __name__)


def _display_messages(messages: dict[str, list[str]]) -> None:
    # TODO: move this into toolforge-weld before using it in other clients once the POC is good to go
    error_messages = messages.get("error", [])
    for message in error_messages:
        click.echo(click.style(message, fg="red"), err=True)

    warning_messages = messages.get("warning", [])
    for message in warning_messages:
        click.echo(click.style(message, fg="yellow"), err=True)

    info_messages = messages.get("info", [])
    for message in info_messages:
        click.echo(click.style(message, fg="blue"), err=True)


def handle_error(e: Exception, debug: bool = False) -> None:
    user_error = isinstance(e, ToolforgeUserError)

    prefix = "Error: "
    if not user_error:
        prefix = f"{e.__class__.__name__}: "

    click.echo(click.style(f"{prefix}{e}", fg="red"))

    if debug:
        LOGGER.exception(e)

        if isinstance(e, ToolforgeError):
            print_error_context(e)
    elif not user_error:
        click.echo(
            click.style(
                "Please report this issue to the Toolforge admins if it persists: https://w.wiki/6Zuu",
                fg="red",
            )
        )


def _format_headers(headers: list[str]) -> list[str]:
    return [click.style(item, bold=True) for item in headers]


@lru_cache(maxsize=None)
def _load_config_from_ctx() -> Config:
    ctx = click.get_current_context()
    return ctx.obj["config"]


@click.version_option(prog_name="Toolforge envvars CLI")
@click.group(name="toolforge", help="Toolforge command line")
@click.option(
    "-v",
    "--verbose",
    help="Show extra verbose output. NOTE: Do no rely on the format of the verbose output",
    is_flag=True,
    default=(os.environ.get("TOOLFORGE_VERBOSE", "0") == "1"),
    hidden=(os.environ.get("TOOLFORGE_CLI", "0") == "1"),
)
@click.option(
    "-d",
    "--debug",
    help=(
        "show logs to debug the toolforge-envvars-* packages. For extra verbose output for say build or "
        "job, see --verbose"
    ),
    is_flag=True,
    default=(os.environ.get("TOOLFORGE_DEBUG", "0") == "1"),
    hidden=(os.environ.get("TOOLFORGE_CLI", "0") == "1"),
)
@click.pass_context
def toolforge_envvars(ctx: click.Context, verbose: bool, debug: bool) -> None:
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["debug"] = debug
    ctx.obj["config"] = get_loaded_config()
    pass


@toolforge_envvars.command(name="list", help="List all your envvars.")
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
@click.option(
    "--truncate/--no-truncate",
    help="Set to '--no-truncate' to display full envvar values.",
    default=True,
    show_default=True,
)
def envvar_list(
    json: bool = False,
    truncate: bool = True,
) -> None:
    config = _load_config_from_ctx()
    envvars_client = EnvvarsClient.from_config(config=config)
    list_response = envvars_client.get("/envvar")
    envvars = list_response
    # TODO: refactor when the API is updated to return the new format
    if "messages" in list_response:
        _display_messages(list_response["messages"])
        envvars = list_response["envvars"]

    if json:
        click.echo(json_mod.dumps(envvars, indent=4))
    else:
        formatted_envvars = [
            [
                envvar["name"],
                (envvar["value"][:50] + "...") if truncate and len(envvar["value"]) > 49 else envvar["value"],
            ]
            for envvar in envvars
        ]
        click.echo(
            tabulate(
                formatted_envvars,
                headers=_format_headers(["name", "value"]),
                tablefmt="plain",
            )
        )


@toolforge_envvars.command(name="show", help="Show a specific envvar.")
@click.argument("ENVVAR_NAME", required=True)
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
def envvar_show(
    envvar_name: str,
    json: bool = False,
) -> None:
    config = _load_config_from_ctx()
    envvars_client = EnvvarsClient.from_config(config=config)
    get_response = envvars_client.get(f"/envvar/{envvar_name}")
    envvar = get_response
    # TODO: refactor when the API is updated to return the new format
    if "messages" in get_response:
        envvar = get_response["envvar"]
        _display_messages(get_response["messages"])

    if json:
        click.echo(json_mod.dumps(envvar, indent=4))
    else:
        click.echo(
            tabulate(
                [[envvar["name"], envvar["value"]]],
                headers=_format_headers(["name", "value"]),
                tablefmt="plain",
            )
        )


def _should_prompt():
    "For easy mocking"
    return sys.stdin.isatty()


def read_value(ctx: click.Context, param: click.Parameter, value: Any) -> str:
    if value is not None:
        return value

    if _should_prompt():
        value = click.prompt("Enter the value of your envvar (Hit Ctrl+C to cancel)")
    else:
        value = sys.stdin.read()

    return value


@toolforge_envvars.command(name="create", help="Create/update an envvar.")
@click.argument("ENVVAR_NAME", required=True)
@click.argument("ENVVAR_VALUE", required=False, callback=read_value)
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
def envvar_create(
    envvar_name: str,
    envvar_value: str | None,
    json: bool = False,
) -> None:
    config = _load_config_from_ctx()
    envvars_client = EnvvarsClient.from_config(config=config)
    create_response = envvars_client.post(f"/envvar/{envvar_name}", json={"value": envvar_value})
    envvar = create_response
    # TODO: refactor when the API is updated to return the new format
    if "messages" in create_response:
        envvar = create_response["envvar"]
        _display_messages(create_response["messages"])

    if json:
        click.echo(json_mod.dumps(envvar, indent=4))
    else:
        click.echo(
            tabulate(
                [[envvar["name"], envvar["value"]]],
                headers=_format_headers(["name", "value"]),
                tablefmt="plain",
            )
        )


@toolforge_envvars.command(name="delete", help="Delete an envvar.")
@click.argument("ENVVAR_NAME", required=True)
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
@click.option(
    "--yes-im-sure",
    help="If set, will not ask for confirmation",
    is_flag=True,
)
def envvar_delete(
    envvar_name: str,
    json: bool = False,
    yes_im_sure: bool = False,
) -> None:
    config = _load_config_from_ctx()

    if not yes_im_sure:
        if not click.prompt(
            text=f"Are you sure you want to delete {envvar_name}? (this can't be undone) [yN]",
            default="no",
            show_default=False,
            type=lambda val: val.lower() in ["y", "Y", "1", "yes", "true"],
        ):
            click.echo("Aborting at user's request")
            sys.exit(1)

    envvars_client = EnvvarsClient.from_config(config=config)
    delete_response = envvars_client.delete(f"/envvar/{envvar_name}")
    envvar = delete_response
    # TODO: refactor when the API is updated to return the new format
    if "messages" in delete_response:
        envvar = delete_response["envvar"]
        _display_messages(delete_response["messages"])

    if json:
        click.echo(json_mod.dumps(envvar, indent=4))
    else:
        click.echo(f"Deleted {envvar_name}, here is its last value: ")
        click.echo(
            tabulate(
                [[envvar["name"], envvar["value"]]],
                headers=_format_headers(["name", "value"]),
                tablefmt="plain",
            )
        )


@toolforge_envvars.command(name="quota", help="Get envvars quota information.")
@click.option(
    "--json",
    help="If set, will output in json format",
    is_flag=True,
)
def envvar_quota(
    json: bool = False,
) -> None:
    config = _load_config_from_ctx()
    envvars_client = EnvvarsClient.from_config(config=config)
    quota_response = envvars_client.get("/quota")
    quota = quota_response
    # TODO: refactor when the API is updated to return the new format
    if "messages" in quota_response:
        quota = quota_response["quota"]
        _display_messages(quota_response["messages"])

    if json:
        click.echo(json_mod.dumps(quota, indent=4))
    else:
        formatted_quota = [[quota["quota"], quota["used"], quota["quota"] - quota["used"]]]

        click.echo(
            tabulate(
                formatted_quota,
                headers=_format_headers(["quota", "used", "available"]),
                tablefmt="plain",
            )
        )


def main() -> int:
    # this is needed to setup the logging before the subcommand discovery
    res = toolforge_envvars.parse_args(ctx=click.Context(command=toolforge_envvars), args=sys.argv)
    debug = "-d" in res or "--debug" in res
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        toolforge_envvars()
    except subprocess.CalledProcessError as e:
        handle_error(e, debug=debug)
        return e.returncode
    except Exception as e:
        handle_error(e, debug=debug)
        return 1

    return 0


if __name__ == "__main__":
    main()
