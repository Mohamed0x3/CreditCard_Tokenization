from modules.Project_def import *


# =================================================
# TODO (TAHER|HELMY \ SAMIR)
def Merchant_App_1(client_socket_app):
    # data = {
    #     "flag": True,
    #     "message": "",
    #     "transactions": transactions,
    #     "merchant": merchant,
    # }
    # data["message"] = "Here is available Transactions"
    # data["transaction number"] = "?"
    # sendData(client_socket_app, data)
    # data = receiveData(client_socket_app)
    # transaction = transactions[data["transaction number"]]
    #################
    data = {
        "flag": True,
        "transaction":{"transactionID": '11111',
        "price": 120,},
        
        "merchant": merchant,
    }
    sendData(client_socket_app, data)

# TODO (TAHER|HELMY \ HEFNEY)


def Merchant_Bank_1(BANK_PORT):
    client_socket_bank = requestConnection(BANK_PORT)
    data = receiveData(client_socket_bank)
    print(f"{data}")
    data["message"] = "merchant"
    sendData(client_socket_bank, data)
    data = receiveData(client_socket_bank)

    data["merchant"] = merchant  # TODO
    data["transaction"] = transaction  # TODO
    data["token"] = card  # TODO
    sendData(client_socket_bank, data)
    data = receiveData(client_socket_bank)
    if data["flag"] is False:
        print(f"invalid transaction... try again")

    approved_transaction = data["approved"]
# TODO (TAHER|HELMY \ SAMIR)


def Merchant_App_2(client_socket_app):
    data["approved"] = approved_transaction


# This function do handshake with the app then send data of the merchant to the app
def Merchant_App_1_admin(client_socket_app):
    data = "Merchant say \"Hello\" to App"
    sendData(client_socket_app, data)
    data = receiveData(client_socket_app)  # "App reply \"Hello\" to Merchant"
    print(data)
    Merchant_App_1(client_socket_app)
    # sendData(client_socket_app, merchant)

    print("sent merchant and transaction data to app")
    # data = receiveData(client_socket_app) #"App give \"token\" to Merchant"
    # print(data)


def Merchant_Bank_admin(BANK_PORT):
    client_socket_bank = requestConnection(BANK_PORT)
    print(f"Connected to the bank")
    data = receiveData(client_socket_bank)
    print(data)  # "Bank say \"Hello\" to Merchant"
    data = "Merchant reply \"Hello\" to Bank"
    sendData(client_socket_bank, data)
    data = "Merchant give \"token\" to Bank"
    sendData(client_socket_bank, data)
    data = receiveData(client_socket_bank)
    print(data)  # "Bank say \"Transaction is ok\" to Merchant"


def Merchant_App_2_admin(client_socket_app):
    data = "\"Transaction is ok\" Merchant and App are Friends?"
    sendData(client_socket_app, data)
    # "Merchant and App are Friends?... YES"
    data = receiveData(client_socket_app)
    print(data)
# =================================================


merchant = {"name": "Merchant1", "number": "1212121212121212", "exp_month": 9,
            "exp_year": 2025}  # TODO
transactions = ["TODO", "TODO1", "TODO1"]  # TODO
transaction = ""
approved_transaction = False

token = ""

# ======================== THREAD 1
# Merchant act as a server with the PayAPP (THREAD TODO - HELMY)
print(f"Openning The Store... (please wait)")

merchant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
merchant_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
merchant_socket.bind((IP, MERCHANT_PORT))
merchant_socket.listen()

sockets_list = [merchant_socket]

clients = {}

print(f"Store Open...")

while False:  # TODO (SET True)
    client_socket_app = acceptConnection(merchant_socket)

    Merchant_App_1(client_socket_app)

    # TODO HERE Merchant talk with the bank (WAIT THREAD 2)
    # ======================== THREAD 2 (Start)
    # Merchant act as a client with the bank

    Merchant_Bank_1(BANK_PORT)

    # TODO: Merchant BACK TO THREAD 1
    # TODO Rerturn from thread 2
    # ======================== THREAD 2 (End)

    Merchant_App_2(client_socket_app)

client_socket_app = acceptConnection(merchant_socket)
Merchant_App_1_admin(client_socket_app)
# Merchant_Bank_admin(BANK_PORT)
# Merchant_App_2_admin(client_socket_app)
