def cbrt(x) -> float | complex:
    """
    Return the cubic root of x.
    """
    from .constants import pi
    from .sqrt import sqrt
    from .atan import atan
    from .exp import exp
    if type(x) is complex:
        a = x.real
        b = x.imag
        if a != 0:
            r = sqrt(a**2+b**2)
            if a > 0 and b > 0:
                theta = atan(b/a)
            elif a > 0 and b < 0:
                theta = 2*pi-atan(-b/a)
            elif a < 0 and b > 0:
                theta = pi - atan(b/-a)
            elif a < 0 and b < 0:
                theta = pi + atan(-b/-a)
            elif a > 0 and b == 0:
                theta = 0
            else:
                theta = 3*pi
            low = 0.0
            high = max(1.0, r)
            epsilon = 0.00000000000001
            while True:
                mid = (low + high)/2
                mid_cubed = mid * mid * mid

                if abs(mid_cubed-r) < epsilon:
                    cubed_r = mid
                    break
                elif mid_cubed < r:
                    low = mid
                else:
                    high = mid
            principal_root = cubed_r * exp(theta*1j/3)
            if abs(principal_root.imag) < 1e-8:
                return principal_root.real
            return principal_root
            
        if b >= 0:
            low = 0.0
            high = max(1.0, b)
        else:
            low = min(-1.0, b)
            high = 0.0
        
        epsilon = 0.00000000000001
    
        while True:
            mid = (low + high) / 2
            mid_cubed = mid * mid * mid

            if abs(mid_cubed - b) < epsilon:
                cubed_b = mid
                break
            elif mid_cubed < b:
                low = mid
            else:
                high = mid
        return cubed_b*-1j
    if x >= 0:
        low = 0.0
        high = max(1.0, x)
    else:
        low = min(-1.0, x)
        high = 0.0
    
    epsilon = 1e-10
    
    while True:
        mid = (low + high) / 2
        mid_cubed = mid * mid * mid

        if abs(mid_cubed - x) < epsilon:
            return mid
        elif mid_cubed < x:
            low = mid
        else:
            high = mid
