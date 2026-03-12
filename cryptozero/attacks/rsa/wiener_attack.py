from math import isqrt

from cryptozero.attacks.base import CipherAttack
from cryptozero.ciphers.rsa import RSA

class WienerAttack(CipherAttack):
    def is_vulnerable(self) -> bool:
        n = self.params.get('n')
        e = self.params.get('e')
        if n is None or e is None:
            return False
        try:
            _ = self._find_d(n, e)
            return True
        except ValueError:
            return False

    def _continued_fraction(self, a: int, b: int) -> list[int]:
        cf = []
        while b:
            cf.append(a // b)
            a, b = b, a - (a // b) * b
        return cf

    def _convergents(self, cf: list[int]):
        num, den = 1, 0
        prev_num, prev_den = 0, 1
        for q in cf:
            num, prev_num = q * num + prev_num, num
            den, prev_den = q * den + prev_den, den
            yield (num, den)

    def _find_d(self, n: int, e: int) -> int:
        cf = self._continued_fraction(e, n)
        for k, d in self._convergents(cf):
            if k == 0 or (e * d - 1) % k != 0:
                continue
            phi = (e * d - 1) // k
            s = n - phi + 1
            disc = s * s - 4 * n
            if disc >= 0:
                t = isqrt(disc)
                if t * t == disc:
                    return d
        raise ValueError("Wiener attack failed: d not found")

    def run(self, ciphertext: bytes) -> bytes:
        n = self.params.get('n')
        e = self.params.get('e')

        if n is None or e is None:
            raise ValueError("Missing parameters: 'n' and 'e' are required for run")

        d = self._find_d(n, e)
        rsa = RSA(n=n, e=e, d=d)

        return rsa.decrypt(ciphertext)
