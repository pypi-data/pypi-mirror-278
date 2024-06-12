import click
from ..output.table import output_entry
from . import policy_config


@click.command(name="get-authz-bundle")
@click.pass_context
@click.option("--org-id", default=None)
@click.option("--if-none-match", default=None)
def cli_command_get_authz_bundle(ctx, **kwargs):
    result, status, headers = policy_config.get_authz_bundle(ctx, **kwargs)
    output_entry(ctx, result.to_dict(), headers)


@click.command(name="delete-authz-bundle")
@click.pass_context
@click.option("--org-id", default=None)
def cli_command_delete_authz_bundle(ctx, **kwargs):
    policy_config.delete_authz_bundle(ctx, **kwargs)


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
