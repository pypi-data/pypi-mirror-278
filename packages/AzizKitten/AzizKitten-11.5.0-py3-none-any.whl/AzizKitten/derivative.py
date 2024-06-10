def derivative(func, value) -> float | complex:
    """
    Return the derivative of a function 'func' at a specific value.
    """
    h=1e-10
    ans=(func(value+h)-func(value))/h
    return ans