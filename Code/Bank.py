from modules.Project_def import *
from Bank_implementation import *

# =============================

def Bank_Communication_App_admin_2(client_socket_app):
    data = receiveData_RSA(client_socket_app,PAYMENT_KEY,BANK_KEY)
    print(f"Decrypted data:\n{data}")

    # NOTE: TOKENIZATION
    # NOTE: From
    # token = bytes(str(bank.tokenize(data["card"]["number"], data["card"]["cvv"], data["merchant"]
    #               ["merchant_id"], data["transaction"]["transactionID"])), encoding="utf-8")
    # NOTE: to
    token = str(bank.tokenize(data["card"]["number"], data["card"]["cvv"], data["merchant"]
                  ["merchant_id"], data["transaction"]["transactionID"]))
    # NOTE: End - to
    print("sending encrypted token to the app")
    # encryped = encrypt(token, PAYMENT_KEY.publickey())
    # sendData(client_socket_app, encryped)
    sendData_RSA(client_socket_app, token,BANK_KEY,PAYMENT_KEY)


def Bank_Communication_App_admin_1():
    client_socket_app = acceptConnection(bank_socket)
    print("sending hello signal to app")
    data = "Bank say \"Hello\" to App"
    sendData_RSA(client_socket_app, data,BANK_KEY,PAYMENT_KEY)
    data = receiveData_RSA(client_socket_app,PAYMENT_KEY,BANK_KEY)  # "App reply \"Hello\" to Bank"
    print(data)
    Bank_Communication_App_admin_2(client_socket_app)



def Bank_Communication_Merchant_admin_2():
    client_socket_Merchant = acceptConnection(bank_socket)
    data = "Bank say \"Hello\" to Merchant"
    print("sending hello signal to merchant..")
    sendData_RSA(client_socket_Merchant, data, BANK_KEY, MERCHANT_KEY)
    # "Merchant reply \"Hello\" to Bank"
    data = receiveData_RSA(client_socket_Merchant, MERCHANT_KEY, BANK_KEY)
    print(data)
    # "Merchant give \"token\" to Bank"
    # NOTE: From
    # data = receiveData(client_socket_Merchant)
    # print(f"received encrypted token\n {data}")
    # decrypted = decrypt(ast.literal_eval(str(data)), BANK_KEY)
    # decrypted = json.loads(decrypted.decode())
    # NOTE: to
    decrypted = receiveData_RSA(client_socket_Merchant, MERCHANT_KEY, BANK_KEY)
    # NOTE: End - to

    print(f"Decrypted token\n{decrypted}")
    res = bank.transact(decrypted["token"], decrypted["transaction"]["price"],
                        decrypted["merchant_id"], decrypted["transaction"]["transactionID"])
    # do transaction
    # data = "Bank say \"Transaction is ok\" to Merchant"
    sendData_RSA(client_socket_Merchant, res,BANK_KEY, MERCHANT_KEY)

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
