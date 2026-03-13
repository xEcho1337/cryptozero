class DiffieHellman:
    def __init__(self, p: int, g: int):
        self.p = p
        self.g = g

    def public_key(self, private):
        return pow(self.g, private, self.p)

    def shared_secret(self, private, other_public):
        return pow(other_public, private, self.p)