from math import isqrt

def _continued_fraction(a: int, b: int) -> list[int]:
    cf = []
    while b:
        cf.append(a // b)
        a, b = b, a - (a // b) * b
    return cf

def _convergents(cf: list[int]):
    num, den = 1, 0
    prev_num, prev_den = 0, 1
    for q in cf:
        num, prev_num = q * num + prev_num, num
        den, prev_den = q * den + prev_den, den
        yield num, den

def wiener_attack(n: int, e: int) -> int | None:
    cf = _continued_fraction(e, n)
    for k, d in _convergents(cf):
        if k == 0 or (e * d - 1) % k != 0:
            continue

        phi = (e * d - 1) // k
        s = n - phi + 1
        disc = s * s - 4 * n

        if disc >= 0:
            t = isqrt(disc)
            if t * t == disc:
                return d

    return None