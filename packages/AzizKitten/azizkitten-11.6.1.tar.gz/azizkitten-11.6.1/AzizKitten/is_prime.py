def is_prime(x: int) -> bool:
    if x != int(x) or x < 0:
        raise ValueError("Value input must be positive integer.")
    if int(x) == 2 or int(x) == 3:
        return True
    if int(x) % 5 != 0 and int(x) % 7 != 0:
        if (int(x) + 1) % 6 == 0 or (int(x) - 1) % 6 == 0:
            return True
    return False