import click

from simplelogincmd.cli import const


@click.command(
    "toggle",
    short_help=const.HELP.ALIAS.CONTACT.TOGGLE.SHORT,
    help=const.HELP.ALIAS.CONTACT.TOGGLE.LONG,
)
@click.argument(
    "id",
)
def toggle(id: str) -> bool:
    """Enable or disable a contact"""
    from simplelogincmd.cli.commands.alias_commands.contact_commands._toggle import (
        _toggle,
    )

    return _toggle(id)
