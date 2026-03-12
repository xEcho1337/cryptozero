from pathlib import Path

def read_bytes(path: str) -> bytes:
    return Path(path).read_bytes()

def write_bytes(path: str, data: bytes) -> None:
    Path(path).write_bytes(data)

def hex_dump(b: bytes, width: int = 16) -> str:
    lines = []
    for i in range(0, len(b), width):
        chunk = b[i:i+width]
        hexstr = " ".join(f"{c:02x}" for c in chunk)
        ascii_str = ''.join(chr(c) if 32 <= c < 127 else '.' for c in chunk)
        lines.append(f"{i:08x}: {hexstr:<{width*3}} {ascii_str}")
    return "\n".join(lines)