import math
import sympy.ntheory.modular

from collections import Counter
from gmpy2 import is_prime, next_prime
from sympy import factorint, integer_nthroot, Matrix


def egcd(a: int, b: int) -> tuple[int,int,int]:
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def inverse(a: int, m: int) -> int:
    return pow(a, -1, m)


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def ithroot(a: int, b: int) -> int:
    return integer_nthroot(a, b)


def crt(moduli: list[int], residues: list[int]) -> tuple[int, int] | None:
    return sympy.ntheory.modular.crt(moduli, residues)


def compute_phi(factors: list[int]) -> int:
    counts = Counter(factors)
    phi = 1

    for p, e in counts.items():
        phi *= (p ** e - p ** (e - 1))  # oppure p**(e-1) * (p - 1)

    return phi


def vandermonde(xs: list[int], degree: int, mod: int):
    return Matrix([
        [pow(x, j, mod) for j in range(degree + 1)]
        for x in xs
    ])


def interpolate_mod(xs: list[int], ys: list[int], mod: int):
    assert len(xs) == len(ys), "xs e ys must have the same length"

    n = len(xs)

    A = vandermonde(xs, n - 1, mod)
    b = Matrix(ys)

    # A * coeffs = b mod p
    coeffs = A.inv_mod(mod) * b

    return [int(c % mod) for c in coeffs]


def smooth_prime(starting: int, bits: int, unique=False) -> int:
    if not is_prime(starting):
        raise ValueError("Starting value is not prime")

    pm1 = starting - 1
    factors = factorint(pm1)
    last = max(factors)

    while pm1.bit_length() < bits:
        last = next_prime(last)
        pm1 *= last

    k = last if unique else 0
    while True:
        k += 1

        if unique and not is_prime(k):
            continue

        test = k * pm1 + 1
        if is_prime(test):
            return test


def baby_step_giant_step(g: int, b: int, p: int, order: int) -> int | None:
    m = math.isqrt(order)
    if m * m < order:
        m += 1

    table = {}
    value = 1

    for j in range(m):
        table[value] = j
        value = (value * g) % p

    factor = pow(g, -m, p)

    y = b % p
    for i in range(m):
        j = table.get(y)
        if j is not None:
            return (i * m + j) % order
        y = (y * factor) % p

    return None
