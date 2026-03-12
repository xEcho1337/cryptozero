import socket
from typing import Optional

# TODO: improve this
class Netcat:
    """
    Simple wrapper for netcat-like connections.

    Methods:
    - `receive_until(delimiter: bytes) -> bytes`: read from the socket until the delimiter is found.
    - `send(data: bytes) -> None`: send data over the socket.
    """
    def __init__(self, host: str, port: int, timeout: float = 10.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock: Optional[socket.socket] = None

    def _connect(self) -> None:
        if self.sock is None:
            self.sock = socket.create_connection((self.host, self.port), self.timeout)

    def send(self, data: bytes) -> None:
        """Send data to the remote service."""
        self._connect()
        assert self.sock is not None
        self.sock.sendall(data)

    def receive_until(self, delimiter: bytes) -> bytes:
        """Receive from the service until the buffer ends with `delimiter`."""
        self._connect()
        assert self.sock is not None
        buffer = b""
        while not buffer.endswith(delimiter):
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            buffer += chunk
        return buffer

    def close(self) -> None:
        """Close the connection."""
        if self.sock:
            self.sock.close()
            self.sock = None
