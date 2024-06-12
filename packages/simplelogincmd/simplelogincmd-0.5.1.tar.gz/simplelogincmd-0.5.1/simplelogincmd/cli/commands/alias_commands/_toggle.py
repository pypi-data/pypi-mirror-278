import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Alias


def _toggle(id):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    if (alias := input.resolve_id(db, Alias, id)) is not None:
        id = alias.id

    success, result = sl.toggle_alias(id)
    if not success:
        click.echo(result)
        return False

    if alias is not None:
        # Update local db.
        alias.enabled = result
        db.session.add(alias)
        db.session.commit()

    click.echo("Enabled" if result else "Disabled")
    return True
