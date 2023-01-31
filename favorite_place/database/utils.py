def update_query(document: dict) -> dict:
    """
    Make a single-level query from a nested object for updating in the Mongo database.

    Example:
    >>> update_query({"a": {"b": 1}, "c": {"d": 2, "e": {"f":3}, "g": 4}, "h": 5})
    {'a.b': 1, 'c.d': 2, 'c.e.f': 3, 'c.g': 4, 'h': 5}
    """
    query = {}
    for key, value in document.items():
        if isinstance(value, dict):
            query.update(update_field(key, value))
        else:
            query[key] = value
    return query


def update_field(field: str, document: dict) -> dict:
    """
    Make a single-level query from a nested object for a field.

    Example:
    >>> update_field(
    ...     "field_name",
    ...     {"a": {"b": 1}, "c": {"d": 2, "e": {"f":3}, "g": 4}, "h": 5}
    ... )
    {
        'field_name.a.b': 1,
        'field_name.c.d': 2,
        'field_name.c.e.f': 3,
        'field_name.c.g': 4,
        'field_name.h': 5
    }
    """
    update = {}
    for key, value in document.items():
        if isinstance(value, dict):
            update.update(update_field(field, update_field(key, value)))
        else:
            update[f"{field}.{key}"] = value
    return update
