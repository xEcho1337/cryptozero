from sympy import factorint
from sympy.ntheory.modular import crt
from tqdm import tqdm
from cryptozero.attacks.base import CipherAttack

class PohligHellman(CipherAttack):
    """
    Pohlig-Hellman algorithm to find a discrete logarithm
    when the modulus p is B-smooth, i.e. when p-1 has small factors.

    This attack requireas specifying 3 parameters:

    - g: The generator
    - h: The number for which to find the discrete logarithm
    - p: The prime modulus
    """
    def is_vulnerable(self) -> bool:
        p = self.params.get('p')

        if p is None:
            raise ValueError("Parameter 'p' is required for Pohlig-Hellman")

        factors = factorint(p - 1, limit=10 ** 7)
        biggest = max(factors)

        return biggest.bit_length() > 32

    def run(self, ciphertext: bytes) -> bytes:
        p = self.params.get('p')
        g = self.params.get('g')
        h = self.params.get('h')
        limit = self.params.get('limit')

        if p is None:
            raise ValueError("Parameter 'p' is required for Pohlig-Hellman")

        if g is None:
            raise ValueError("Parameter 'g' is required for Pohlig-Hellman")

        if h is None:
            raise ValueError("Parameter 'h' is required for Pohlig-Hellman")

        if limit is None:
            limit = 10 ** 7

        n = p - 1
        factors = factorint(n, limit=limit)

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

        x = crt(moduli, residues)[0]
        return x
