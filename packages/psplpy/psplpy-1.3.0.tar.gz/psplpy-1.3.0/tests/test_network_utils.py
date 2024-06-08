import socket
import threading

if __name__ == '__main__':
    from __init__ import *
else:
    from . import *
from psplpyProject.psplpy.network_utils import ClientSocket, ServerSocket


def get_ip_address():
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("114.114.114.114", 80))  # connect to a public ip address
        ip_address = temp_socket.getsockname()[0]  # get the host's ip
        temp_socket.close()
        return ip_address
    except socket.error:
        return None


port = 12351
client_port = 54333
data = b"Hello World" * 1024 * 32


def sender():
    def handler(client_socket: ClientSocket, addr):
        print(addr)
        assert addr == (get_ip_address(), client_port)

        received_data = client_socket.recv()
        assert received_data == data
        client_socket.send(data)
        recv_tmp_file = tmp_dir / 'recv_tmp.tmp'
        client_socket.recvf(recv_tmp_file)
        assert tmp_file.read_text() == recv_tmp_file.read_text()

        tmp_file.unlink()
        recv_tmp_file.unlink()
        client_socket.close()
        server.close()

    server = ServerSocket(port=port)
    server.handle(handler)


def recver():
    client = ClientSocket(port=port, client_host=get_ip_address(), client_port=client_port)
    client.connect()
    client.send(data)
    received_data = client.recv()
    assert received_data == data
    tmp_file.write_bytes(data)
    client.sendf(tmp_file)
    client.close()


def tests():
    threading.Thread(target=sender).start()
    threading.Thread(target=recver).start()


if __name__ == '__main__':
    tests()
