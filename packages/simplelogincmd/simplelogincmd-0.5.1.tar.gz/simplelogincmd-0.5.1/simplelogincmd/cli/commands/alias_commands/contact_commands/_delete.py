import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Contact


def _delete(id, bypass_confirmation):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    if (contact := input.resolve_id(db, Contact, id)) is not None:
        id = contact.id
        name = contact.contact
    else:
        name = id

    if not bypass_confirmation:
        click.confirm(f"Delete {name}?", abort=True)

    success, msg = sl.delete_contact(id)
    if not success:
        # Clarify the somewhat vague error message
        msg = f"Unknown ID {id}" if msg == "Forbidden" else msg
        click.echo(msg)
        return False

    if contact is not None:
        # Update local db.
        db.session.delete(contact)
        db.session.commit()

    return True
