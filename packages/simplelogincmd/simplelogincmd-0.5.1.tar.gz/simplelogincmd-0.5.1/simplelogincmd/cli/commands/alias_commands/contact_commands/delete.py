import click

from simplelogincmd.cli import const


@click.command(
    "delete",
    short_help=const.HELP.ALIAS.CONTACT.DELETE.SHORT,
    help=const.HELP.ALIAS.CONTACT.DELETE.LONG,
)
@click.argument(
    "id",
)
@click.option(
    "-y",
    "--yes",
    "bypass_confirmation",
    is_flag=True,
    flag_value=True,
    default=False,
    help=const.HELP.ALIAS.CONTACT.DELETE.OPTION.YES,
)
def delete(id: str, bypass_confirmation: bool) -> bool:
    """Delete a contact"""
    from simplelogincmd.cli.commands.alias_commands.contact_commands._delete import (
        _delete,
    )

    return _delete(id, bypass_confirmation)
