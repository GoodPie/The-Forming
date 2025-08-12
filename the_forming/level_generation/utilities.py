def clamp(value, a, b):
    """Clamp value to the inclusive range [a, b]."""
    if value < a:
        value = a
    elif value > b:
        value = b

    return value
