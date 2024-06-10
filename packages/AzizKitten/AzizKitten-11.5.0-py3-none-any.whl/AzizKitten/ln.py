def ln(x) -> float | complex:
    """
    Return the natural logarithm of x.
    """
    from .exp import exp
    from .constants import pi
    if x == 0:
        raise ValueError("Value input must be different to 0.")
    if x > 0:
        if x == 1:
            return 0
        y = x
        while True:
            f = exp(y) - x
            f_prime = exp(y)
            if abs(f_prime) < 1e-6:
                y += 1
            else:
                y -= f/f_prime
                if abs(f) < 1e-12:
                    return y
    y = abs(x)
    if abs(x) == 1:
        return pi*1j
    while True:
            f = exp(y) - abs(x)
            f_prime = exp(y)
            if abs(f_prime) < 1e-6:
                y += 1
            else:
                y -= f/f_prime
                if abs(f) < 1e-12:
                    return y + pi*1j