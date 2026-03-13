from sympy import factorint
from sympy.ntheory.modular import crt
from tqdm import tqdm

def pohlig_hellman(p: int, g: int, h: int, limit=10 ** 7) -> bytes:
    n = p - 1
    factors = factorint(n, limit=limit)

    if max(factors) > limit:
        raise Exception("Biggest factor exceeds limit")

    residues = []
    moduli = []

    for q, e in tqdm(factors.items(), desc="Searching Discrete Logarithm"):
        qe = q ** e
        exp = n // qe

        g_i = pow(g, exp, p)
        h_i = pow(h, exp, p)

        x_qe = 0

        # Handle cases where the exponent is not 1
        dlog = None

        for d in range(q):
            if pow(g_i, d, p) == h_i:
                dlog = d
                break

        if dlog is None:
            raise Exception("Discrete logarithm not found")

        for k in range(e):
            x_qe += dlog * (q ** k)

        residues.append(x_qe)
        moduli.append(qe)

    x, n = crt(moduli, residues)[0]
    return x
