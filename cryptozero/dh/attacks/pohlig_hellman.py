from sympy import factorint, n_order
from sympy.ntheory.modular import crt
from tqdm import tqdm

def pohlig_hellman(g: int, h: int, p: int):
    n = n_order(g, p)
    factors = factorint(n)

    residues = []
    moduli = []

    for q, e in tqdm(factors.items(), desc="Searching Discrete Log"):
        x = 0

        for k in range(e):
            exp = n // (q ** (k + 1))

            g_k = pow(g, exp, p)
            gx = pow(g, x, p)
            inv = pow(gx, -1, p)

            t = pow((h * inv) % p, exp, p)

            for d in range(q):
                if pow(g_k, d, p) == t:
                    x += d * (q ** k)
                    break

        residues.append(x)
        moduli.append(q ** e)

    return crt(moduli, residues)[0]