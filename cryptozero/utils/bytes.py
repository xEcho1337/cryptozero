def to_int(b: bytes, byteorder: str = "big", signed: bool = False) -> int:
    return int.from_bytes(b, byteorder, signed=signed)

def from_int(i: int, length: int = None, byteorder: str = "big") -> bytes:
    if length is None:
        length = (i.bit_length() + 7) // 8 or 1
    return i.to_bytes(length, byteorder)

def chunk_bytes(b: bytes, size: int) -> list[bytes]:
    return [b[i:i+size] for i in range(0, len(b), size)]