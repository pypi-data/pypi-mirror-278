import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


def _list(id, include, exclude, header):
    fields = util.output.get_display_fields_from_options(
        const.CONTACT_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return

    cfg = util.init.cfg()
    sl = util.init.sl(cfg)
    db = util.init.db(cfg)
    if (alias := util.input.resolve_id(db, Alias, id)) is not None:
        id = alias.id

    contacts = sl.get_all_alias_contacts(id)
    if len(contacts) == 0:
        click.echo("No contacts found")
        return

    # Update local db.
    for contact in contacts:
        db.session.upsert(contact)
    db.session.commit()

    pager_threshold = cfg.get("display.pager-threshold")
    if header is None:
        header = cfg.get("display.headers")
    util.output.display_model_list(
        contacts,
        fields,
        pager_threshold,
        header,
    )
