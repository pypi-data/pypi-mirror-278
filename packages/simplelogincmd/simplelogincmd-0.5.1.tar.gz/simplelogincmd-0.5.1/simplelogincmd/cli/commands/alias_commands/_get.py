import click

from simplelogincmd.cli import const, util
from simplelogincmd.database.models import Alias


def _get(id, include, exclude, header):
    fields = util.output.get_display_fields_from_options(
        const.ALIAS_FIELD_ORDER, include, exclude
    )
    if len(fields) == 0:
        return

    cfg = util.init.cfg()
    sl = util.init.sl(cfg)
    db = util.init.db(cfg)
    if (alias := util.input.resolve_id(db, Alias, id)) is not None:
        id = alias.id

    success, obj = sl.get_alias(id)
    if not success:
        click.echo(obj)
        return None

    # Update local db.
    db.session.upsert(obj)
    db.session.commit()

    if header is None:
        header = cfg.get("display.headers")
    util.output.display_model_list(
        [obj],
        fields,
        pager_threshold=0,
        header=header,
    )
