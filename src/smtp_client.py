import base64
from socket import *

socket = socket(AF_INET, SOCK_STREAM)


def connect():
    server = input("Server: ")
    port = input("Port for Mailserver: ")
    socket.connect((server, int(port)))


def get():
    return socket.recv(1024).decode()


def getHelo():
    socket.send("EHLO SR\r\n".encode())
    return socket.recv(1024).decode()


def login():
    username = input("Username: ")
    password = input("Password: ")
    encoded = base64.b64encode(("\x00" + username + "\x00" + password).encode())
    login_data = "AUTH PLAIN ".encode() + encoded + "\r\n".encode()
    socket.send(login_data)
    print(socket.recv(1024).decode())


def worker():
    connect()
    # print(getHelo())
    login()
    sender = input("Sender-Email: ")
    socket.send(("MAIL FROM:<" + sender + ">\r\n").encode())
    print(socket.recv(1024).decode())
    receiver = input("Reciever-Email: ")
    socket.send(("RCPT TO:<" + receiver + ">\r\n").encode())
    print(socket.recv(1024).decode())
    mailtext = input("Mailtext: ")
    mailtext = mailtext + "\r\n\r\n"
    socket.send(("DATA\r\n").encode())
    print(socket.recv(1024).decode())
    socket.send(mailtext.encode())


worker()
