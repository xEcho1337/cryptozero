from math import isqrt

def fermat_attack(n: int, max_iter=10000) -> tuple[int, int] | tuple[None, None]:
    a = isqrt(n)

    if a * a < n:
        a += 1
    for _ in range(max_iter):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            p = a - b
            q = a + b
            return p, q
        a += 1
    return None, None
