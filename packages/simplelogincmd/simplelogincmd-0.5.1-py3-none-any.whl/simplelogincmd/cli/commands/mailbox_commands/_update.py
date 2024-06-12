import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Mailbox


def _update(id, email, default, cancel_email_change):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    if (mailbox := input.resolve_id(db, Mailbox, id)) is not None:
        id = mailbox.id

    success, msg = sl.update_mailbox(id, email, default, cancel_email_change)
    if not success:
        click.echo(msg)
        return False

    if mailbox is not None:
        # Update local db.
        mailbox.email = email or mailbox.email
        mailbox.default = default or mailbox.default
        db.session.add(mailbox)
        db.session.commit()

    return True
