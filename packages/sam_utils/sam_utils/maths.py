def is_even(num: int | float):
    """
    Checks if a number is even.

    :param num: The number to compare against.
    :returms: `True`, if the number is even, `False` if the number is odd.
    """
    if num % 2 == 0:
        return True
    return False

def is_numeric(thing):
    """
    Checks if a thing is a number integers or floats.

    :param thing: The object you want to compare against.
    :returns: `True` if the object is an integer or a float, `False` if the object is not.
    """
    if isinstance(thing, (int, float)):
        return True
    return False

def is_positive(num: int | float):
    """
    Checks if a number is positive.
    
    :param num: The number you want to check.
    :returns: `True` if the number is positive, `False` if not.
    """
    if is_numeric(num):
        if num > 0:
            return True
    return False