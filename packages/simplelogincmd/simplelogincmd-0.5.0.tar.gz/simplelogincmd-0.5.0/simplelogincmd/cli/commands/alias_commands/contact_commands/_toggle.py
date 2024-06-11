import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Contact


def _toggle(id):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    id = input.resolve_id(db, Contact, id)
    success, result = sl.toggle_contact(id)
    if not success:
        click.echo(result)
        return False
    click.echo("Blocked" if result else "Unblocked")
    return True
