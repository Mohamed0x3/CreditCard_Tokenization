import socket
import select
import errno
import sys
import pickle

HEADER_SIZE = 10
IP = "127.0.0.1"
APP_PORT = 1234
BANK_PORT = 1235
MERCHANT_PORT = 1236


def receiveData(client_socket):
    # Receive Data
    full_msg = b""
    new_msg = True
    while True:
        msg = client_socket.recv(16)  # buffer >= HEADER_SIZE
        if new_msg:
            msglen = int(msg[:HEADER_SIZE])
            new_msg = False

        full_msg += msg

        if len(full_msg) - HEADER_SIZE == msglen:
            d = pickle.loads(full_msg[HEADER_SIZE:])
            return d


def requestConnection(PORT):
    # Connect to PORT
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    return client_socket


def acceptConnection(my_socket):
    client_socket, address = my_socket.accept()
    print(f"Connection from {address} has been established!")

    return client_socket


def sendData(client_socket, data):
    msg = pickle.dumps(data)
    msg = bytes(f"{len(msg):<{HEADER_SIZE}}", "utf-8") + msg

    client_socket.send(msg)
