import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Alias


def _delete(id, bypass_confirmation):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    if (alias := input.resolve_id(db, Alias, id)) is not None:
        id = alias.id
        name = alias.email
    else:
        name = id

    if not bypass_confirmation:
        click.confirm(f"Delete {name}?", abort=True)

    success, msg = sl.delete_alias(id)
    if not success:
        # Clarify the somewhat vague error message
        msg = f"Unknown ID {id}" if msg == "Forbidden" else msg
        click.echo(msg)
        return False

    if alias is not None:
        # Update local db.
        db.session.delete(alias)
        db.session.commit()

    return True
