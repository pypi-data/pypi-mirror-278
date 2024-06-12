import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Alias


def _create(id, email):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    if (alias := input.resolve_id(db, Alias, id)) is not None:
        id = alias.id

    success, obj = sl.create_contact(id, email)
    if not success:
        click.echo(obj)
        return False

    # Update local db.
    db.session.upsert(obj)
    db.session.commit()

    click.echo(obj.reverse_alias_address)
    return True
