import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Contact


def _delete(id, bypass_confirmation):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    id = input.resolve_id(db, Contact, id)
    if not bypass_confirmation:
        contact = db.session.get(Contact, id)
        msg = f"Delete {contact.contact if contact else id}?"
        click.confirm(msg, abort=True)
    success, msg = sl.delete_contact(id)
    if not success:
        # Clarify the somewhat vague error message
        msg = f"Unknown ID {id}" if msg == "Forbidden" else msg
        click.echo(msg)
        return False
    return True
