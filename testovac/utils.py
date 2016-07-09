def is_true(value):
    """
    Converts GET parameter value to bool
    """
    if isinstance(value, bool):
        return value
    return bool(value) and value.lower() not in ('false', '0')
