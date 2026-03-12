from math import isqrt

from cryptozero.attacks.base import CipherAttack
from cryptozero.ciphers.rsa import RSA


class FermatAttack(CipherAttack):
    """
    Fermat's attack for N = p*q with p and q close together.
    """
    def is_vulnerable(self) -> bool:
        p, q = self.get_factors()
        return p is not None and q is not None

    def get_factors(self, max_iter=10000):
        n = self.params.get('n')
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

    def run(self, ciphertext: bytes) -> bytes:
        n = self.params.get('n')
        p, q = self.get_factors()

        phi = (p - 1) * (q - 1)
        e = self.params.get('e')
        d = pow(e, -1, phi)

        rsa = RSA(n=n, e=e, d=d)
        return rsa.decrypt(ciphertext)
