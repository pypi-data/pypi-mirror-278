import click

from simplelogincmd.cli import const


@click.command(
    "list",
    short_help=const.HELP.MAILBOX.LIST.SHORT,
    help=const.HELP.MAILBOX.LIST.LONG,
    epilog=const.HELP.MAILBOX.LIST.EPILOG,
)
@click.option(
    "-i",
    "--include",
    help=const.HELP.MAILBOX.LIST.OPTION.INCLUDE,
)
@click.option(
    "-e",
    "--exclude",
    help=const.HELP.MAILBOX.LIST.OPTION.EXCLUDE,
)
@click.option(
    "--header/--no-header",
    "header",
    default=None,
    help=const.HELP.MAILBOX.LIST.OPTION.HEADER,
)
def list(
    include: str,
    exclude: str,
    header: bool | None,
) -> None:
    """Display mailboxes in a tabular format"""
    from simplelogincmd.cli.commands.mailbox_commands._list import _list

    return _list(include, exclude, header)
