from modules.Project_def import *
from Bank_implementation import *

# =============================
# TODO (SAMIR / HEFENY / TAHER|HELMY)


def Bank_Communication():
    while True:
        client_socket = acceptConnection(bank_socket)
        data = {"flag": True, "message": ""}
        data["message"] = "app or merchant"
        data["type"] = "?"
        sendData(client_socket, data)
        data = receiveData(client_socket)
        print(f"{data}")

        if data["type"] == "app":
            data["message"] = "please fill required fields"
            data["card"] = "?"
            data["merchant"] = "?"
            data["transaction"] = "?"
            valid = False
            while not valid:
                sendData(client_socket, data)
                data = receiveData(client_socket)
                # Validate given data in db
                # TODO (HEFNY)
                if "TODO" == "TODO":
                    valid = True
                    # (True) Send Token
                    # TODO (HEFNY)
                    token = "TODO"
                    data["token"] = token
                # (False) Send Fail... try again
                else:
                    data["flag"] = False
                    data["message"] = "data is wrong.. try again"

        elif data["type"] == "merchant":
            data["message"] = "please fill required fields"
            data["merchant"] = "?"
            data["transaction"] = "?"
            data["token"] = "?"
            valid = False
            while not valid:
                sendData(client_socket, data)
                data = receiveData(client_socket)
                # Validate given data in db
                # (True) Send transaction happend
                if "TODO" == "TODO":  # TODO (HEFNY)
                    valid = True
                    data["approved"] = True
                # (False) Send Fail... try again
                else:
                    data["flag"] = False
                    data["approved"] = False
                    data["message"] = "data is wrong.. try again"


def Bank_Communication_App_admin_2(client_socket_app):
    data = receiveData(client_socket_app)
    print("Received encrypted data from app:\n")
    print(data)
    decrypted = decrypt(ast.literal_eval(str(data)), BANK_KEY)
    data = json.loads(decrypted.decode())
    print(f"Decrypted data:\n{data}")
    token = bytes(str(bank.tokenize(data["card"]["number"], data["card"]["cvv"], data["merchant"]
                  ["merchant_id"], data["transaction"]["transactionID"])), encoding="utf-8")
    print("sending encrypted token to the app")
    encryped = encrypt(token, PAYMENT_KEY.publickey())
    sendData(client_socket_app, encryped)


def Bank_Communication_App_admin_1():
    client_socket_app = acceptConnection(bank_socket)
    print("sending hello signal to app")
    data = "Bank say \"Hello\" to App"
    sendData(client_socket_app, data)
    data = receiveData(client_socket_app)  # "App reply \"Hello\" to Bank"
    print(data)
    Bank_Communication_App_admin_2(client_socket_app)
    # data = "Bank give \"token\" to App"
    # sendData(client_socket_app, data)


def Bank_Communication_Merchant_admin_2():
    client_socket_Merchant = acceptConnection(bank_socket)
    data = "Bank say \"Hello\" to Merchant"
    print("sending hello signal to merchant..")
    sendData(client_socket_Merchant, data)
    # "Merchant reply \"Hello\" to Bank"
    data = receiveData(client_socket_Merchant)
    print(data)
    # "Merchant give \"token\" to Bank"
    data = receiveData(client_socket_Merchant)
    print(f"received encrypted token\n {data}")
    decrypted = decrypt(ast.literal_eval(str(data)), BANK_KEY)
    decrypted = json.loads(decrypted.decode())

    print(f"Decrypted token\n{decrypted}")
    res = bank.transact(decrypted["token"], decrypted["transaction"]["price"],
                        decrypted["merchant_id"], decrypted["transaction"]["transactionID"])
    # do transaction
    # data = "Bank say \"Transaction is ok\" to Merchant"
    sendData(client_socket_Merchant, res)

# =============================


print(f"Openning The Bank... (please wait)")
bank = Bank()

bank_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bank_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bank_socket.bind((IP, BANK_PORT))
bank_socket.listen()

sockets_list = [bank_socket]

clients = {}

print(f"Bank Open...")


# Bank act as a server with the PayApp
# Bank act as a server with the Merchant

# Bank_Communication()
Bank_Communication_App_admin_1()
Bank_Communication_Merchant_admin_2()
