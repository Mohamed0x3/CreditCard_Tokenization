from modules.Project_def import *
from Bank_implementation import *

# =============================

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
Bank_Communication_App_admin_1()
Bank_Communication_Merchant_admin_2()
