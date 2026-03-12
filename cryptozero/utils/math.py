def egcd(a: int, b: int) -> tuple[int,int,int]:
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def inverse(a: int, m: int) -> int:
    return pow(a, -1, m)

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a