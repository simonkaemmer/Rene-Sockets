import socket
from struct import *

HOST = "127.0.0.1"
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()


def get_data(bytedata):
    n = unpack('I 7s B', bytedata[0:12])[2]
    fstr = 'I7sB'
    for i in range(n):
        fstr = fstr + 'i'

    print(fstr + "\n")
    return unpack(fstr, bytedata)


def do_sum(a):
    return sum(a)


def do_prod(a):
    result = 1
    for x in a:
        result = result * x
    return result


def do_min(a):
    return min(a)


def do_max(a):
    return max(a)


conn, addr = s.accept()
with conn:
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        data = get_data(data)
        intlist = data[3:]
        operation = str(data[1]).replace("\\x00", "")
        operation = operation.replace("'", "")
        operation = operation.replace("b", "")
        print("Operation: " + operation)

        if not data:
            break

        if operation == "Summe":
            fresult = do_sum(intlist)
            conn.sendall(pack('Ii', data[0], fresult))
            break
        elif operation == "Produkt":
            fresult = do_prod(intlist)
            conn.sendall(pack('Ii', data[0], fresult))
            break
        elif operation == "Minimum":
            fresult = do_min(intlist)
            conn.sendall(pack('Ii', data[0], fresult))
            break
        elif operation == "Maximum":
            fresult = do_max(intlist)
            conn.sendall(pack('Ii', data[0], fresult))
            break
        else:
            break

    conn.close()
