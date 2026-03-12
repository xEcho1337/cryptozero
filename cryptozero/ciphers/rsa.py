from Crypto.Util.number import bytes_to_long, long_to_bytes

class RSA:
    """
    Class for basic RSA operations.
    """
    def __init__(self, n: int, e: int, d: int = None):
        self.n = n
        self.e = e
        self.d = d

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Performs c = m^e mod n on plaintext (bytes) and returns ciphertext (bytes).
        """
        m_int = bytes_to_long(plaintext)
        c_int = pow(m_int, self.e, self.n)
        return long_to_bytes(c_int)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypts ciphertext (bytes) using d: m = c^d mod n.
        Requires that d is set.
        """
        if self.d is None:
            raise ValueError("Private exponent 'd' is missing for decrypt")
        c_int = bytes_to_long(ciphertext)
        m_int = pow(c_int, self.d, self.n)
        return long_to_bytes(m_int)
