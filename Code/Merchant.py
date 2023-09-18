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
#  then send transaction approval to the Payment App
def Merchant_Bank_admin(client_socket_bank, token):

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

    # send transaction approval to Paymaent App
    print(f"Merchant: sending [ Transaction approval( \"{data}\" ) ] to the App")
    sendData_RSA(client_socket_app, data,MERCHANT_KEY, PAYMENT_KEY)
    data = receiveData_RSA(client_socket_app, PAYMENT_KEY, MERCHANT_KEY)
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
print("=======================================\n")


client_socket_app = acceptConnection(merchant_socket)
print("Payment App is connecting...")
token = Merchant_Com_App(client_socket_app)

print("\n=======================================\n")

client_socket_bank = requestConnection(BANK_PORT)
Merchant_Bank_admin(client_socket_bank, token)
