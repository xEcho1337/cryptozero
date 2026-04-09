import base64
import urllib.parse

def from_ascii(s: str, encoding: str = "utf-8") -> bytes:
    return s.encode(encoding)


def to_ascii(b: bytes, encoding: str = "utf-8") -> str:
    return b.decode(encoding, errors="replace")


def from_base64(s: str) -> bytes:
    return base64.b64decode(s)


def to_base64(b: bytes) -> str:
    return base64.b64encode(b).decode()


def from_hex(s: str) -> bytes:
    s = s.strip().lower()
    if s.startswith("0x"):
        s = s[2:]
    if len(s) % 2:
        s = "0" + s
    return bytes.fromhex(s)


def to_hex(b: bytes, prefix: bool = False) -> str:
    h = b.hex()
    return ("0x" + h) if prefix else h


def from_int(i: int, length: int = None, byteorder: str = "big") -> bytes:
    if length is None:
        length = (i.bit_length() + 7) // 8 or 1
    return i.to_bytes(length, byteorder)


def to_int(b: bytes, byteorder: str = "big", signed: bool = False) -> int:
    return int.from_bytes(b, byteorder, signed=signed)


def from_url(s: str) -> bytes:
    return urllib.parse.unquote_to_bytes(s)


def to_url(b: bytes) -> str:
    return urllib.parse.quote_from_bytes(b)


def chunk_bytes(b: bytes, size: int) -> list[bytes]:
    return [b[i:i+size] for i in range(0, len(b), size)]
