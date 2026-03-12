from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from typing import Union, Any

def load_pem_private_key(data: bytes, password: Union[bytes, None] = None) -> Any:
    """
    Load a PEM or DER private key (PKCS#8 or Traditional OpenSSL).
    Returns a private key object (RSAPrivateKey, etc.).
    """
    try:
        return serialization.load_pem_private_key(data, password=password, backend=default_backend())
    except ValueError:
        # Try DER
        return serialization.load_der_private_key(data, password=password, backend=default_backend())


def load_pem_public_key(data: bytes) -> Any:
    """
    Load a PEM or DER public key (SubjectPublicKeyInfo).
    Returns a public key object (RSAPublicKey, etc.).
    """
    try:
        return serialization.load_pem_public_key(data, backend=default_backend())
    except ValueError:
        # Try DER
        return serialization.load_der_public_key(data, backend=default_backend())


def private_key_to_der(key: Any) -> bytes:
    """
    Serialize a private key to DER PKCS#8.
    """
    return key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


def public_key_to_der(key: Any) -> bytes:
    """
    Serialize a public key to DER SubjectPublicKeyInfo.
    """
    return key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
