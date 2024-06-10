def integrate(integrand, lower_limit, upper_limit) -> float:
    """
    Return the result of the integral of 'integrand' from 'lower_limit' to 'upper_limit'.
    """
    if upper_limit == float('inf'):
        upper_limit = 999999999999999
    if upper_limit == float('-inf'):
        upper_limit = -999999999999999
    if lower_limit == float('inf'):
        lower_limit = 999999999999999
    if lower_limit == float('-inf'):
        lower_limit = -999999999999999
    segment_width = (upper_limit - lower_limit) / 60000
    result = 0.5 * (integrand(lower_limit) + integrand(upper_limit))
    for i in range(1,60000):
        x_i = lower_limit + i * segment_width
        result += integrand(x_i)
    result *= segment_width
    if result >= 1e10:
        return float('inf')
    elif result <= -1e10:
        return float('-inf')
    return result