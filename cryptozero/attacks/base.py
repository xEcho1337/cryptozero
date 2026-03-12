from abc import ABC, abstractmethod

class CipherAttack(ABC):
    def __init__(self, **params):
        self.params = params

    @abstractmethod
    def is_vulnerable(self) -> bool:
        pass

    @abstractmethod
    def run(self, ciphertext: bytes) -> bytes:
        pass
