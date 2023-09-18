from modules.Project_def import *
from Bank_implementation import *

# =============================


# NOTE: Bank accept App connection 
#  then Bank do handshake with the App
#  then App send [merchant, transaction] data
#  then Bank do tokenization
#  then Bank send token to App
def Bank_Com_App():
    
    # Bank accept App connection 
    client_socket_app = acceptConnection(bank_socket)
    
    # Handshake (Bank - App)
    print("sending hello signal to app")
    data = "Bank say \"Hello\" to App"
    sendData_RSA(client_socket_app, data,BANK_KEY,PAYMENT_KEY)
    data = receiveData_RSA(client_socket_app,PAYMENT_KEY,BANK_KEY)  # "App reply \"Hello\" to Bank"
    print(data)
    
    # receive [merchant, transaction] data
    data = receiveData_RSA(client_socket_app,PAYMENT_KEY,BANK_KEY)
    print(f"Decrypted data:\n{data}")

    # do Tokenization
    token = str(bank.tokenize(data["card"]["number"], data["card"]["cvv"], data["merchant"]
                  ["merchant_id"], data["transaction"]["transactionID"]))
    
    # Send token to app
    print("sending encrypted token to the app")
    sendData_RSA(client_socket_app, token,BANK_KEY,PAYMENT_KEY)



# NOTE: Bank accept Merchant connection
#  then Bank do handshake with the Merchant
#  then Merchant send [merchant - transaction - token] data
#  then Bank do transaction
#  then Bank send transaction approval to Merchant 
def Bank_Com_Merchant():
    
    # Accept Merchant connection
    client_socket_Merchant = acceptConnection(bank_socket)
    
    # Handshake (Bank - Merchant)
    data = "Bank say \"Hello\" to Merchant"
    print("sending hello signal to merchant..")
    sendData_RSA(client_socket_Merchant, data, BANK_KEY, MERCHANT_KEY) 
    data = receiveData_RSA(client_socket_Merchant, MERCHANT_KEY, BANK_KEY) # "Merchant reply \"Hello\" to Bank"
    print(data)
    
    # receive [merchant - transaction - token] data from Merchant
    decrypted = receiveData_RSA(client_socket_Merchant, MERCHANT_KEY, BANK_KEY)
    print(f"Decrypted token\n{decrypted}")
    
    # do transaction
    res = bank.transact(decrypted["token"], decrypted["transaction"]["price"],
                        decrypted["merchant_id"], decrypted["transaction"]["transactionID"])
    
    # send transaction approval to Merchant 
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
Bank_Com_App()
Bank_Com_Merchant()
