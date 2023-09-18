from modules.Project_def import *
from Bank_implementation import *
from modules.Sequence_comm_def import *

# =============================


# NOTE: Bank accept App connection 
#  then Bank do handshake with the App
#  then App send [merchant, transaction] data
#  then Bank do tokenization
#  then Bank send token to App
def Bank_Com_App():

    # Bank accept App connection 
    client_socket_app = acceptConnection(bank_socket)
    
    print("Payment App is connecting...")
    # Handshake (Bank - App)
    Handshake_server_Com(client_socket_app, "Bank")
    
    print("\n=======================================")
    print("waiting for [card, merchant, transaction]...\n")
    # receive [card, merchant, transaction] data
    data = receiveData_RSA(client_socket_app,PAYMENT_KEY,BANK_KEY)
    print(f"Received required data...")
    print(f"Card info:[ {data['card']} ] \nmerchant: [ {data['merchant']} ] \ntransaction: [ {data['transaction']} ]")
    
    # do Tokenization
    print("Tokenization is running...")
    token = str(bank.tokenize(data["card"]["number"], data["card"]["cvv"], data["merchant"]
                  ["merchant_id"], data["transaction"]["transactionID"]))
    print("Tokenization is done...")
    
    # Send token to app
    print(f"Bank: sending [ {token} ] to the Payment App")
    sendData_RSA(client_socket_app, token,BANK_KEY,PAYMENT_KEY)



# NOTE: Bank accept Merchant connection
#  then Bank do handshake with the Merchant
#  then Merchant send [merchant - transaction - token] data
#  then Bank do transaction
#  then Bank send transaction approval to Merchant 
def Bank_Com_Merchant():
    
    # Accept Merchant connection
    client_socket_Merchant = acceptConnection(bank_socket)
    
    print("Merchant is connecting...")
    # Handshake (Bank - Merchant)
    Handshake_server_Com(client_socket_Merchant, "Bank")
    
    print("\n=======================================")
    print("waiting for [token, merchant, transaction]...\n")
    # receive [merchant - transaction - token] data from Merchant
    data = receiveData_RSA(client_socket_Merchant, MERCHANT_KEY, BANK_KEY)
    print(f"Received required data...")
    print(f"Token:[ {data['token']} ] \nMerchant_id: [ {data['merchant_id']} ] \ntransaction: [ {data['transaction']} ]")
    
    # do transaction
    print("\nTransaction proccess is running...")
    res = bank.transact(data["token"], data["transaction"]["price"],
                        data["merchant_id"], data["transaction"]["transactionID"])
    print("Transaction proccess is done...\n")
    
    # send transaction approval to Merchant 
    print(f"Bank: sending transaction approval:[ \"{res}\" ] to the Payment App")
    sendData_RSA(client_socket_Merchant, res,BANK_KEY, MERCHANT_KEY)

# =============================

###############################################################################################################
####################################################################### Main ########################################################################
###############################################################################################################


mode = -1
print("This Module has two modes\n",
      "\t(1) If you want this module to run as Normal\n",
      "\t(2) If you want this module to simulte action to hacker(act as merchant)")
mode = input("Enter mode number\n")
while mode != "1" and mode != "2":
    print("invalid input, Please try again...")
    mode = input("Enter mode number\n")

print("===================================================")
print("===================    Loading     ================")
print("===================================================\n")

print(f"Openning The Bank... (please wait)")
bank = Bank()
bank_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bank_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bank_socket.bind((IP, BANK_PORT))
bank_socket.listen()
sockets_list = [bank_socket]

clients = {}

print(f"Bank Open...")
print("=======================================\n")

if mode == "1":

    # Bank act as a server with the PayApp
    # Bank act as a server with the Merchant
    Bank_Com_App()
    Bank_Com_Merchant()

else:
    # Bank act as a server with the Merchant
    Bank_Com_Merchant()

