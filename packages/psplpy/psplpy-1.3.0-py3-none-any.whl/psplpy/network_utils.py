import errno
import socket
import threading
import time
from pathlib import Path
from typing import Any, Callable


class ClientSocket:
    def __init__(self, host: str = '127.0.0.1', port: int = 12345, client_socket: socket.socket = None,
                 client_host: str = None, client_port: int = 12345):
        self.host = host
        self.port = port
        self.client_host = client_host
        self.client_port = client_port
        self.client_socket = client_socket

        self._length_bytes = 5

        if self.client_socket:
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32 * 1024 * 1024)

    def connect(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32 * 1024 * 1024)
        # use the certain address of the client to connect the server
        if self.client_host and self.client_port:
            self.client_socket.bind((self.client_host, self.client_port))
        self.client_socket.connect((self.host, self.port))

    def _get_length(self, data: bytes) -> bytes:
        # for 5 bytes unsigned int, the max data length is 2**40 - 1, namely about 1tb
        bytes_result = len(data).to_bytes(self._length_bytes, byteorder='big')
        return bytes_result

    def _recv_length(self) -> int:
        byte_result = self.client_socket.recv(self._length_bytes)
        return int.from_bytes(byte_result, byteorder='big')

    def send(self, data: bytes):
        return self.client_socket.sendall(self._get_length(data) + data)

    def recv(self) -> bytes:
        length = self._recv_length()
        data = bytearray()
        while len(data) < length:
            data += self.client_socket.recv(length - len(data))
        return bytes(data)

    def recvf(self, output_path: str | Path, bufsize: int = 1024 * 1024 * 16) -> None:
        with open(output_path, 'wb') as f:
            while True:
                data = self.client_socket.recv(bufsize)
                if not data:
                    break
                f.write(data)

    def sendf(self, input_path: str | Path, bufsize: int = 1024 * 1024 * 16) -> None:
        with open(input_path, 'rb') as f:
            while True:
                data = f.read(bufsize)
                if not data:
                    break
                self.client_socket.send(data)

    def close(self) -> None:
        return self.client_socket.close()


class ServerSocket:
    def __init__(self, host: str = '127.0.0.1', port: int = 12345, backlog: int = 64):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(backlog)
        self.server_socket.setblocking(False)

    def accept(self) -> tuple[ClientSocket, Any] | tuple[None, None]:
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                return ClientSocket(client_socket=client_socket), addr
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK or e.errno == errno.EAGAIN:
                    time.sleep(0.01)
                    continue
                elif e.errno == errno.EBADF:
                    return None, None
                else:
                    raise e

    def handle(self, handler: Callable, *args, **kwargs) -> None:
        def _handle():
            while True:
                client_socket, addr = self.accept()
                if not (client_socket and addr):
                    break
                handle_thread = threading.Thread(target=handler, args=(client_socket, addr, *args), kwargs=kwargs)
                handle_thread.daemon = True
                handle_thread.start()
        threading.Thread(target=_handle).start()

    def close(self) -> None:
        self.server_socket.close()
