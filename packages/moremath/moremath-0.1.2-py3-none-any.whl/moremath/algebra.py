from typing import Union


def exponentiation(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
    """Calculate exponentiation of a base to a given exponent."""
    if not isinstance(base, (int, float)) or not isinstance(exponent, (int, float)):
        raise TypeError("Both base and exponent must be integers or floats")
    return base ** exponent


def logarithm(x: Union[int, float], base: Union[int, float] = 10) -> Union[float, complex]:
    """Calculate logarithm of x with a specified base."""
    if not isinstance(x, (int, float)):
        raise TypeError("x must be an integer or float")
    if not isinstance(base, (int, float)):
        raise TypeError("Base must be an integer or float")

    if x <= 0:
        raise ValueError("x must be greater than 0")

    if base <= 0 or base == 1:
        raise ValueError("Base must be greater than 0 and not equal to 1")

    from math import log
    return log(x, base)