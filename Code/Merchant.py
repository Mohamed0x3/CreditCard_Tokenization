from modules.Project_def import *


# =================================================

# NOTE: This function sends [Merchant, Transaction] to Payment App
def Merchant_App_1(client_socket_app):
    data = {
        "flag": True,
        "transaction": transaction,

        "merchant": merchant,
    }

    payload = json.dumps(data).encode()
    encrypted = encrypt(payload, PAYMENT_KEY.publickey())
    sendData(client_socket_app, encrypted)


# NOTE:
#       This function do handshake with the app
#  then send data of the merchant to the app
#  then Receive Token
def Merchant_App_1_admin(client_socket_app):
    data = "Merchant say \"Hello\" to App"
    print("sending hello to app..")
    sendData(client_socket_app, data)
    data = receiveData(client_socket_app)  # "App reply \"Hello\" to Merchant"
    print(data)
    Merchant_App_1(client_socket_app)
    # sendData(client_socket_app, merchant)

    print("sent merchant and transaction data encrypted to app")
    print("waiting for the token")
    data = receiveData(client_socket_app)
    print(f"Got encrypted token:\n {data}")
    decrypted = decrypt(ast.literal_eval(str(data)), MERCHANT_KEY)
    print(f"Decrypted token:\n {decrypted}")

    return decrypted
    # data = receiveData(client_socket_app) #"App give \"token\" to Merchant"
    # print(data)

# NOTE:
#       This function do handshake with the bank
#  then Merchant send token and Merchant data to the bank
#  then Receive transaction approval
#  then send transaction approval to the Payment App
def Merchant_Bank_admin(client_socket_bank, token):
    print(f"Connected to the bank")
    data = receiveData(client_socket_bank)
    print(data)  # "Bank say \"Hello\" to Merchant"
    print("sending reply signal to bank")
    data = "Merchant reply \"Hello\" to Bank"
    sendData(client_socket_bank, data)
    # data = "Merchant give \"token\" to Bank"
    print("sending encrypted token to the bank")
    data = {"token": token.decode("utf-8"),
            "merchant_id": str(merchant["merchant_id"]), "transaction": transaction}
    # print(data)
    payload = json.dumps(data).encode()
    enToken = encrypt(payload, BANK_KEY.publickey())
    sendData(client_socket_bank, enToken)
    data = receiveData(client_socket_bank)
    print(data)  # "Bank say \"Transaction is ok\" to Merchant"

    Merchant_App_2_admin(client_socket_app, data)


# NOTE: Send transaction approval to Paymaent App
def Merchant_App_2_admin(client_socket_app, data):
    # data = "\"Transaction is ok\" Merchant and App are Friends?"
    sendData(client_socket_app, data)
    # "Merchant and App are Friends?... YES"
    data = receiveData(client_socket_app)
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
