from modules.Project_def import *

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

def Bank_Communication_App_admin_1():
    client_socket_app = acceptConnection(bank_socket)
    data = "Bank say \"Hello\" to App"
    sendData(client_socket_app, data)
    data = receiveData(client_socket_app) # "App reply \"Hello\" to Bank"
    print(data)
    data = "Bank give \"token\" to App"
    sendData(client_socket_app, data)
def Bank_Communication_Merchant_admin_2():
    client_socket_Merchant = acceptConnection(bank_socket)
    data = "Bank say \"Hello\" to Merchant"
    sendData(client_socket_Merchant, data)
    data = receiveData(client_socket_Merchant) # "Merchant reply \"Hello\" to Bank"
    print(data)
    data = receiveData(client_socket_Merchant) # "Merchant give \"token\" to Bank"
    print(data)
    data = "Bank say \"Transaction is ok\" to Merchant"
    sendData(client_socket_Merchant, data)

# =============================

print(f"Openning The Bank... (please wait)")

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
