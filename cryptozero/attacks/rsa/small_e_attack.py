from cryptozero.attacks.base import CipherAttack
from cryptozero.encodings.int import to_int

class SmallEAttack(CipherAttack):
    def is_vulnerable(self) -> bool:
        n = self.params.get('n')
        e = self.params.get('e')
        if n is None or e is None:
            return False
        return e <= 5

    def run(self, ciphertext: bytes) -> bytes:
        c = to_int(ciphertext)
        e = self.params.get('e')

        m = int(round(c ** (1 / e)))
        plaintext = m.to_bytes((m.bit_length() + 7) // 8, 'big')

        return plaintext
