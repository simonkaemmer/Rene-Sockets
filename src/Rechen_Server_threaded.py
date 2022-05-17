import socket
import threading
from _thread import *
from struct import *

print_lock = threading.Lock()


def threaded(c):
    while True:

        data = c.recv(1024)
        if not data:
            print_lock.release()
            break
        data = get_data(data)
        intlist = data[3:]
        operation = str(data[1]).replace("\\x00", "")
        operation = operation.replace("'", "")
        operation = operation.replace("b", "")
        print("Operation: " + operation)

        if operation == "Summe":
            fresult = do_sum(intlist)
            c.sendall(pack('Ii', data[0], fresult))
            break
        elif operation == "Produkt":
            fresult = do_prod(intlist)
            c.sendall(pack('Ii', data[0], fresult))
            break
        elif operation == "Minimum":
            fresult = do_min(intlist)
            c.sendall(pack('Ii', data[0], fresult))
            break
        elif operation == "Maximum":
            fresult = do_max(intlist)
            c.sendall(pack('Ii', data[0], fresult))
            break

    print_lock.release()
    print("Ready for next")
    c.close()


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


def Main():
    host = ""
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    s.listen(5)
    print("Listeing...")

    while True:
        c, addr = s.accept()

        print_lock.acquire(timeout=10.0)
        print("Connected to :", addr[0], ":", addr[1])
        start_new_thread(threaded, (c,))


if __name__ == '__main__':
    Main()
