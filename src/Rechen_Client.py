import socket
from struct import *

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = pack('I 7s B i i', 1, "Maximum".encode(), 2, 1, 12)
    s.sendall(message)
    data = s.recv(1024)
    data = unpack('Ii', data)

print(f"Recieved {data!r}")
