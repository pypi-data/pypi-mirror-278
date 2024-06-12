import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import Mailbox


def _delete(id, transfer_aliases_to, bypass_confirm):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    if (mailbox := input.resolve_id(db, Mailbox, id)) is not None:
        id = mailbox.id
        name = mailbox.email
    else:
        name = id

    if not bypass_confirm:
        if transfer_aliases_to == -1:
            click.confirm(
                f"This will delete all of {name}'s aliases. Are you sure?",
                abort=True,
            )
        else:
            click.confirm(f"Delete {name}?", abort=True)

    success, msg = sl.delete_mailbox(id, transfer_aliases_to)
    if not success:
        click.echo(msg)
        return False

    if mailbox is not None:
        # Update local db.
        db.session.delete(mailbox)
        db.session.commit()

    return True
