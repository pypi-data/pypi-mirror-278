import select
import socket
import ssl
import time


def connect_secure(address: str, port: int) -> ssl.SSLSocket:
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.VerifyMode.CERT_NONE
    sock = socket.create_connection((address, port))
    ssock = context.wrap_socket(sock, server_hostname=address)
    ssock.settimeout(0.1)
    return ssock


def connect(address: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    sock.connect((address, port))
    return sock


class NetworkError(Exception):
    pass


class Socket:
    def __init__(self, server: str, port: int, secure: bool):
        if secure:
            self._socket: socket.socket = connect_secure(server, port)
        else:
            self._socket = connect(server, port)
        self._buffer = b""
        self._connect_time = time.time()

    @property
    def socket(self) -> socket.socket:
        return self._socket

    @property
    def connect_time(self) -> float:
        return self._connect_time

    def read(self) -> bytes:
        try:
            sockets = [self._socket]
            ready_to_read, _, _ = select.select(sockets, sockets, sockets, 0.1)
            if len(ready_to_read) > 0:
                data = self._socket.recv(2048)
                if len(data) == 0:
                    raise NetworkError("No data, connection reset by peer?")
                self._buffer += data

            result = self._buffer
            self._buffer = b""
            return result
        except BrokenPipeError as exn:
            raise NetworkError(str(exn)) from exn
        except ConnectionResetError as exn:
            raise NetworkError(str(exn)) from exn
        except ssl.SSLZeroReturnError as exn:
            raise NetworkError(str(exn)) from exn

    def write(self, data: bytes) -> None:
        self._socket.sendall(data)
