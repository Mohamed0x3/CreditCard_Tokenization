from modules.Project_def import *

merchant = {"TODO"}  # TODO
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

while True:
    client_socket = acceptConnection(merchant_socket)
    data = {
        "flag": True,
        "message": "",
        "transactions": transactions,
        "merchant": merchant,
    }
    data["message"] = "Here is available Transactions"
    data["transaction number"] = "?"
    sendData(client_socket, data)
    data = receiveData(client_socket)

    transaction = transactions[data["transaction number"]]

    # TODO HERE Merchant talk with the bank (WAIT THREAD 2)
    data["approved"] = approved_transaction


# ======================== THREAD 2
# Merchant act as a client with the bank
client_socket = getConnection(BANK_PORT)
data = receiveData(client_socket)
print(f"{data}")
data["message"] = "merchant"
sendData(client_socket, data)
data = receiveData(client_socket)


data["merchant"] = merchant  # TODO
data["transaction"] = transaction  # TODO
data["token"] = card  # TODO
sendData(client_socket, data)
data = receiveData(client_socket)
if data["flag"] is False:
    print(f"invalid transaction... try again")

approved_transaction = data["approved"]
# TODO: Merchant BACK TO THREAD 1
