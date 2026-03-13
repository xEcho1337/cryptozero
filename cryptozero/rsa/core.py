from Crypto.Util.number import bytes_to_long, long_to_bytes

class RSA:
    """
    Class for basic RSA operations.
    """
    def __init__(self, n: int, e: int):
        self.n = n
        self.e = e

    def compute_d(self, phi: int) -> int:
        """
        Performs d = phi^e mod n and returns the private key.
        """
        return pow(self.e, -1, phi)

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Performs c = m^e mod n on plaintext (bytes) and returns ciphertext (bytes).
        """
        m_int = bytes_to_long(plaintext)
        c_int = pow(m_int, self.e, self.n)
        return long_to_bytes(c_int)

    def _encrypt(self, m: int) -> int:
        """
        Performs c = m^e mod n on plaintext (integer) and returns ciphertext (integer).
        """
        return pow(m, self.e, self.n)

    def decrypt(self, ciphertext: bytes, d: int) -> bytes:
        """
        Decrypts ciphertext (bytes) using d: m = c^d mod n.
        """
        c_int = bytes_to_long(ciphertext)
        m_int = pow(c_int, d, self.n)

        return long_to_bytes(m_int)

    def _decrypt(self, c: int, d: int) -> int:
        """
        Decrypts ciphertext (integer) using d: m = c^d mod n.
        """
        return pow(c, d, self.n)