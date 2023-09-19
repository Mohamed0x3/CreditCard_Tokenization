from modules.Project_def import *
from modules.Sequence_comm_def import *


# =================================================

# NOTE: Merchant do handshake with the App
#  then send [Merchant - Transaction] to App
#  then Receive Token
def Merchant_Com_App(client_socket_app):
    
    # NFC happens here, Then Merchant send [Merchant, Transaction] to Payment App

    # Handshake (Merchant - Payment App)
    Handshake_server_Com(client_socket_app, "Merchant")

    # send [Merchant - Transaction] data to App
    data = {
        "flag": True,

        "transaction": transaction,
        "merchant": merchant,
    }
    print(f"Merchant: sending [ Merchant({data['merchant']}) - Transaction({data['transaction']}) ]")
    sendData_RSA(client_socket_app, data,MERCHANT_KEY, PAYMENT_KEY)

    print("\n=======================================")
    print("waiting for the token...\n")

    # receive token from Payment App
    data = receiveData_RSA(client_socket_app, PAYMENT_KEY, MERCHANT_KEY)
    print(f"Received token...")

    print(f"token: \n[ {data} ]")
    return data


# NOTE: This function do handshake with the bank
#  then Merchant send token and Merchant data to the bank
#  then Receive transaction approval
def Merchant_Bank_general(client_socket_bank, token):
    print("Connecting to Bank...")
    # Handshake (Merchant - Bank)
    Handshake_client_Com(client_socket_bank, "Merchant")

    # send token and Merchant data to the bank
    print(f"Merchant: sending [ \n\t- Merchant({merchant}) \n\t- transaction({transaction}) \n\t- token({token}) \n\t] to the Bank")
    data = {"token": token,
            "merchant_id": str(merchant["merchant_id"]), "transaction": transaction}
    sendData_RSA(client_socket_bank, data, MERCHANT_KEY, BANK_KEY)
    
    print("\n=======================================")
    print("waiting for the transaction approval...\n")

    # receive transaction approval from the bank
    data = receiveData_RSA(client_socket_bank, BANK_KEY, MERCHANT_KEY)
    print(f"Received transaction approval...")
    print(f"Transaction approval: \"{data}\"")
    return data

# NOTE: Call Merchant_Bank_general
#  then send transaction approval to the Payment App
def Merchant_Bank_admin(client_socket_bank, token):

    data = Merchant_Bank_general(client_socket_bank, token)

    # send transaction approval to Paymaent App
    print(f"Merchant: sending [ Transaction approval( \"{data}\" ) ] to the App")
    sendData_RSA(client_socket_app, data,MERCHANT_KEY, PAYMENT_KEY)
    data = receiveData_RSA(client_socket_app, PAYMENT_KEY, MERCHANT_KEY)
    print(data)



# =================================================

###############################################################################################################
####################################################################### Main ########################################################################
###############################################################################################################
mint=0
tint=0

merchants=[{"merchant_id": 11111111},{"merchant_id": 22222222},{"merchant_id": 33333333},{"merchant_id": 44444444}]

merchant = merchants[mint]
transactions = [{"transactionID": '11111',"price": 100, },{"transactionID": '22222',"price": 1000, },{"transactionID": '33333',"price": 5000, },{"transactionID": '44444',"price": 50000, }]
transaction = transactions[tint]
approved_transaction = False
token = ""

# ========================

mode = -1
print("This Module has two modes\n",
      "\t(1) If you want this module to run as real merchant\n",
      "\t(2) If you want this module to run as hacker(act as merchant)")
mode = input("Enter mode number\n")
while mode != "1" and mode != "2":
    print("invalid input, Please try again...")
    mode = input("Enter mode number\n")

print("===================================================")
print("===================    Loading     ================")
print("===================================================\n")

if mode == "1":
    # Merchant act as a server with the PayAPP
    print(f"Openning The Store... (please wait)")


    merchant_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    merchant_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    merchant_socket.bind((IP, MERCHANT_PORT))
    merchant_socket.listen()

    sockets_list = [merchant_socket]

    clients = {}

    print(f"Store Open...")
    print("=======================================\n")


    client_socket_app = acceptConnection(merchant_socket)
    print("Payment App is connecting...")
    token = Merchant_Com_App(client_socket_app)

    print("\n=======================================\n")

    client_socket_bank = requestConnection(BANK_PORT)
    Merchant_Bank_admin(client_socket_bank, token)
else:
    print("==== Gathering info ====")
    print("Need Merchant data...")
    merchant["merchant_id"] = input("\tEnter - Merchant Id: ")
    print("Need Transaction data...")
    transaction["transactionID"] = int(input("\tEnter - Transaction Id: "))
    transaction["price"] = int(input("\tEnter - Transaction Value: "))
    print("Need Token...")
    token = input("\tEnter - Token: ")

    input("Confirm that Bank is open first...\npress enter key to start...\n")
    input("Are you sure that it's open?...(press enter key to start)\n")

    print("==== Let's get this money ( •̀ᴗ•́ ) ====\n")
    client_socket_bank = requestConnection(BANK_PORT)
    data = Merchant_Bank_general(client_socket_bank, token)
    if data == "Successful Transaction":
        print("\t\t==== [̲̅$̲̅(̲̅ιο̲̅̅ο̲̅̅)̲̅$̲̅] [̲̅$̲̅(̲̅ιο̲̅̅ο̲̅̅)̲̅$̲̅] [̲̅$̲̅(̲̅ιο̲̅̅ο̲̅̅)̲̅$̲̅] ====\n")
        print("\t\t==== (̅_̅_̅_̅(̅_̅_̅_̅_̅_̅_̅_̅_̅̅_̅()ڪے~ ~ ====\n")
    else:
        print("\t\t==== OH NOOOOOOOOOOOO ====\n")
        print("\t\t====     ( 눈_눈)     ====\n")
        print("\t\t====     ( ˃̣̣̥⌓˂̣̣̥)      ====\n\n\n\n")
    