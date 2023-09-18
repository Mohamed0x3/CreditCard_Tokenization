from modules.Project_def import *


# =================================================

# NOTE: This function sends [Merchant - Transaction] to Payment App
def Merchant_App_1(client_socket_app):
    data = {
        "flag": True,
        "transaction": transaction,

        "merchant": merchant,
    }

    sendData_RSA(client_socket_app, data,MERCHANT_KEY, PAYMENT_KEY)


# NOTE: Merchant do handshake with the app
#  then send data of the merchant to the app
#  then Receive Token
def Merchant_App_1_admin(client_socket_app):
    
    # Handshake (Merchant - Payment App)
    data = "Merchant say \"Hello\" to App"
    print("sending hello to app..")
    sendData_RSA(client_socket_app, data,MERCHANT_KEY,PAYMENT_KEY)
    data = receiveData_RSA(client_socket_app,PAYMENT_KEY,MERCHANT_KEY)  # "App reply \"Hello\" to Merchant"
    print(data)

    # NFC happens here, Then Merchant send [Merchant, Transaction] to Payment App
    Merchant_App_1(client_socket_app)

    print("sent merchant and transaction data encrypted to app")
    print("waiting for the token")

    # receive token from Payment App
    data = receiveData_RSA(client_socket_app, PAYMENT_KEY, MERCHANT_KEY)

    print(f"Decrypted token:\n {data}")
    return data


# NOTE: This function do handshake with the bank
#  then Merchant send token and Merchant data to the bank
#  then Receive transaction approval
#  then send transaction approval to the Payment App
def Merchant_Bank_admin(client_socket_bank, token):

    # Handshake (Merchant - Bank)
    print(f"Connected to the bank")
    data = receiveData_RSA(client_socket_bank,BANK_KEY, MERCHANT_KEY)
    print(data)  # "Bank say \"Hello\" to Merchant"
    print("sending reply signal to bank")
    data = "Merchant reply \"Hello\" to Bank"
    sendData_RSA(client_socket_bank, data,MERCHANT_KEY, BANK_KEY)

    # send token and Merchant data to the bank
    print("sending encrypted token to the bank")
    data = {"token": token,
            "merchant_id": str(merchant["merchant_id"]), "transaction": transaction}
    sendData_RSA(client_socket_bank, data, MERCHANT_KEY, BANK_KEY)
    
    # receive transaction approval from the bank
    data = receiveData_RSA(client_socket_bank, BANK_KEY, MERCHANT_KEY)
    print(data)  # "Bank say \"Transaction is ok\" to Merchant"

    # receive transaction approval from the bank
    Merchant_App_2_admin(client_socket_app, data)


# send transaction approval to Paymaent App
def Merchant_App_2_admin(client_socket_app, data):
    sendData_RSA(client_socket_app, data,MERCHANT_KEY, PAYMENT_KEY)
    data = receiveData_RSA(client_socket_app, PAYMENT_KEY, MERCHANT_KEY)
    print(data)


# =================================================


merchant = {"merchant_id": 12123232}  # TODO
transactions = ["TODO", "TODO1", "TODO1"]  # TODO
transaction = {"transactionID": '11111',
               "price": 120, }
approved_transaction = False
token = ""

# ========================
# Merchant act as a server with the PayAPP
print(f"Openning The Store... (please wait)")

merchant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
merchant_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
merchant_socket.bind((IP, MERCHANT_PORT))
merchant_socket.listen()

sockets_list = [merchant_socket]

clients = {}

print(f"Store Open...")

client_socket_app = acceptConnection(merchant_socket)
token = Merchant_App_1_admin(client_socket_app)

client_socket_bank = requestConnection(BANK_PORT)
Merchant_Bank_admin(client_socket_bank, token)
