import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Contact


def _toggle(id):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    if (contact := input.resolve_id(db, Contact, id)) is not None:
        id = contact.id

    success, result = sl.toggle_contact(id)
    if not success:
        click.echo(result)
        return False

    if contact is not None:
        # Update local db.
        contact.block_forward = result
        db.session.add(contact)
        db.session.commit()

    click.echo("Blocked" if result else "Unblocked")
    return True
