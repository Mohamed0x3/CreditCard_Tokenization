import socket
import select
import errno
import sys
import pickle
import math
import random
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import json
import time
from time import sleep

from Crypto.Cipher import PKCS1_OAEP

# ======================================= Guided Mode ===================================
Guided_Mode = True

def SendData_Guid(other_side):
    input(f"press enter to send data to {other_side}...")

def ReceiveData_Guid(other_side):
    print(f"waiting for data from {other_side}...")

# =====================================================================================
# ======================================= Constants ===================================
# =====================================================================================

HEADER_SIZE = 10
IP = "127.0.0.1"
APP_PORT = 1234
BANK_PORT = 1235
MERCHANT_PORT = 1236


# =====================================================================================
# ================================= RSA KEYS ==========================================
# =====================================================================================

def readKeys():
    f = open('./publicKeyAuthority/Bank_key.pem', 'r')
    BankKey = RSA.import_key(f.read())

    f = open('./publicKeyAuthority/Merchant_key.pem', 'r')
    MerchantKey = RSA.import_key(f.read())

    f = open('./publicKeyAuthority/Payment_key.pem', 'r')
    PaymentKey = RSA.import_key(f.read())

    return BankKey, MerchantKey, PaymentKey


BANK_KEY, MERCHANT_KEY, PAYMENT_KEY = readKeys()


# =====================================================================================
# ================================= Receive Data ======================================
# =====================================================================================

# I am the Reciver
def receiveData_RSA(client_socket,  Sender_KEY, Receiver_KEY):

    # Guided Mode
    if Guided_Mode:
        if Sender_KEY == BANK_KEY:
            ReceiveData_Guid("Bank")
        elif Sender_KEY == MERCHANT_KEY:
            ReceiveData_Guid("Merchant")
        elif Sender_KEY == PAYMENT_KEY:
            ReceiveData_Guid("Payment App")
    # Receive
    data = receiveData(client_socket)
    # Decrypt
    plainData = decrypt(ast.literal_eval(str(data)), Receiver_KEY)
    plainData = json.loads(plainData.decode())

    return plainData

def receiveData(client_socket):
    # Receive Data
    full_msg = b""
    new_msg = True
    while True:
        try:
            msg = client_socket.recv(16)  # buffer >= HEADER_SIZE
            if new_msg:
                msglen = int(msg[:HEADER_SIZE])
                new_msg = False
            full_msg += msg
        except:
            print("Sorry, other side is disconnected \nWill close in 5 seconds...")
            time.sleep(1)
            print("Will close in 4 seconds...")
            time.sleep(1)
            print("Will close in 3 seconds...")
            time.sleep(1)
            print("Will close in 2 seconds...")
            time.sleep(1)
            print("Will close in 1 second...")
            time.sleep(1)
            sys.exit()

        if len(full_msg) - HEADER_SIZE == msglen:
            d = pickle.loads(full_msg[HEADER_SIZE:])
            return d


# =====================================================================================
# ==================================== Send Data ======================================
# =====================================================================================

# I am the Sender
def sendData_RSA(client_socket,data, Sender_KEY, Receiver_KEY):

    if Guided_Mode:
        if Receiver_KEY == BANK_KEY:
            SendData_Guid("Bank")
        elif Receiver_KEY == MERCHANT_KEY:
            SendData_Guid("Merchant")
        elif Receiver_KEY == PAYMENT_KEY:
            SendData_Guid("Payment App")
    
    # Encrypt
    payload = json.dumps(data).encode()
    encryptedData = encrypt(payload, Receiver_KEY.publickey())
    # Send
    sendData(client_socket,encryptedData)

def sendData(client_socket, data):
    msg = pickle.dumps(data)
    msg = bytes(f"{len(msg):<{HEADER_SIZE}}", "utf-8") + msg

    client_socket.send(msg)


# =====================================================================================
# ==================================== Connection =====================================
# =====================================================================================


def requestConnection(PORT):
    # Connect to PORT
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

    return client_socket


def acceptConnection(my_socket):
    client_socket, address = my_socket.accept()
    print(f"Connection from {address} has been established!")

    return client_socket


def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{" " * len(title):<{width}}{space}║\n'  # underscore
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)


# =====================================================================================
# ======================================= OLD RSA =====================================
# =====================================================================================


def coprime(a, b):
    return math.gcd(a, b) == 1


def modInverse(a, b):
    for i in range(1, b):
        if (((a % b) * (i % b)) % b == 1):
            return i
    return -1


def encrypt(message, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(message)


def decrypt(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext)


def generatePublicKeys():
    random_generator = Random.new().read
    BankKey = RSA.generate(4096, random_generator)  # generate pub and priv key
    f = open('./publicKeyAuthority/Bank_key.pem', 'wb')
    f.write(BankKey.export_key('PEM'))
    f.close()

    print("Progress info: Bank_key generated")

    random_generator = Random.new().read
    # generate pub and priv key
    MerchantKey = RSA.generate(4096, random_generator)
    f = open('./publicKeyAuthority/Merchant_key.pem', 'wb')
    f.write(MerchantKey.export_key('PEM'))
    f.close()

    print("Progress info: Merchant_key generated")

    random_generator = Random.new().read
    # generate pub and priv key
    PaymentKey = RSA.generate(4096, random_generator)
    f = open('./publicKeyAuthority/Payment_key.pem', 'wb')
    f.write(PaymentKey.export_key('PEM'))
    f.close()
    
    print("Progress info: Payment_key generated")
