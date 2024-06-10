def csch(x) -> float | complex:
    """
    Return the hyperbolic cosecant of x.
    """
    from .sinh import sinh
    return 1/sinh(x)