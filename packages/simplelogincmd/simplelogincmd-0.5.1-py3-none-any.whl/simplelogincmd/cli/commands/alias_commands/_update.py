import click

from simplelogincmd.cli.util import init, input
from simplelogincmd.database.models import (
    Alias,
    Mailbox,
)


def _update(id, note, name, mailboxes, disable_pgp, pinned):
    cfg = init.cfg()
    sl = init.sl(cfg)
    db = init.db(cfg)
    if (alias := input.resolve_id(db, Alias, id)) is not None:
        id = alias.id

    mailbox_ids = set()
    for mb_id in mailboxes:
        mailbox = input.resolve_id(db, Mailbox, mb_id)
        try:
            mailbox_ids.add(mailbox.id)
        except AttributeError:
            mailbox_ids.add(mb_id)

    if note == "_EDIT":
        note = input.edit()

    success, msg = sl.update_alias(
        alias_id=id,
        note=note,
        name=name,
        mailbox_ids=mailbox_ids,
        disable_pgp=disable_pgp,
        pinned=pinned,
    )
    if not success:
        click.echo(msg)
        return False

    if alias is not None:
        # Update local db.
        alias.note = note or alias.note
        alias.name = name or alias.name
        alias.disable_pgp = disable_pgp or alias.disable_pgp
        alias.pinned = pinned or alias.pinned
        db.session.add(alias)
        db.session.commit()

    return True
