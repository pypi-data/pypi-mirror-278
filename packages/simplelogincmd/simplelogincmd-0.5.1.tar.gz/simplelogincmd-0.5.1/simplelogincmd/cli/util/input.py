import click


def edit(msg: str | None = None, *args, **kwargs) -> str | None:
    """
    Allow the user to enter a message via their editor of choice

    :param message: Default message to show in the temporary file. If
        not given, :attr:`~simplelogincmd.cli.const.EDITOR_DEFAULT_MESSAGE`
        is used, defaults to None
    :type message: str, optional
    :param args: Passed directly on to :func:`click.edit`
    :param kwargs: Passed directly on to :func:`click.edit`

    :return: The message entered, with all commented lines removed,
        or None if the user enters a blank message
    :rtype: str|None
    """
    if msg is None:
        from simplelogincmd.cli import const

        msg = const.EDITOR_DEFAULT_MESSAGE
    text = click.edit(msg, *args, **kwargs)
    if text is None:
        return text
    lines = text.splitlines()
    text = []
    for line in lines:
        stripped_line = line.strip()
        if len(stripped_line) == 0 or stripped_line[0] != "#":
            text.append(line)
    return "\n".join(text)


def prompt_choice(text: str, options: list) -> int:
    """
    Prompt the user to choose one of a list of items

    :param text: The prompt to display to the user, below the list of
        options
    :type text: str
    :param options: List of options from which the user can choose
    :type options: list

    :raise ValueError: if `options` is empty

    :return: The index of the item chosen
    :rtype: int
    """
    low, high = 1, len(options)
    if high == 0:
        raise ValueError("No options provided")
    int_range = click.IntRange(low, high)
    click.echo("")
    for index, option in enumerate(options):
        click.echo(f"{index + 1} - {option}")
    text = f"\n{text} ({low}-{high})"
    choice = click.prompt(text, type=int_range, show_choices=True)
    return choice - 1


def resolve_id(db, model_cls, id):
    """
    Search for a single db object id given an identifier

    Call the model classes :meth:`~Object.resolve_identifier` method to
    locate db objects based on the given identifier, which can be any
    value. If multiple results match, ask the user to choose one and
    return the selected object. If one result matches, return
    it directly. If no matches were found, return None.

    :param db: The access layer instance to use for the lookup
    :type db: :class:`~simplelogincmd.database.DatabaseAccessLayer`
    :param model_cls: The type of db object for which to search
    :type model_cls: Type, subclass of
        :class:`~simplelogincmd.database.models.Object`
    :param id: The id to look up
    :type id: Any, usually int or str, as defined by the model class's
        :meth:`~simplelogincmd.database.models.Object.identifier_query`

    :return: The matched object, or None if none matched
    :rtype: :class:`~simplelogincmd.database.models.Object` | None
    """
    results = model_cls.resolve_identifier(db.session, id)
    count = len(results)
    if count == 0:
        return None
    if count == 1:
        return results[0]
    choice = prompt_choice(f"Select {model_cls.__name__}", results)
    return results[choice]
