from modules.Project_def import *
from modules.Payment_def import *
from modules.Sequence_comm_def import *

# NOTE: App do handshake with the Merchant
#  then App get [Merchant - Transaction] data
def App_Com_Merchant_1(client_socket_merchant):
    
    # Handshake (App - Merchant)
    Handshake_client_Com(client_socket_merchant, "App")

    # receive [merchant - transaction - token] data from Merchant
    print("\n=======================================")
    print("waiting for merchant and transaction info...\n")

    data = receiveData_RSA(client_socket_merchant,MERCHANT_KEY, PAYMENT_KEY)
    print(f"Received required data...")
    print(f"Merchant info:[ {data['merchant']} ]\n transaction: [ {data['transaction']} ]")
    
    return data

# NOTE: App send [Card - Merchant - Transaction] data to Bank
#  then App get token from the Bank
def App_Com_Bank(client_socket_bank, card, merchant, transaction):
    
    print("Connecting to Bank...")
    # Handshake (App - Bank)
    Handshake_client_Com(client_socket_bank, "App")

    
    # send [Card - Merchant - Transaction] data to Bank
    print(f"App: sending [ \n\t- Card info({card}) \n\t- merchant info({merchant}) \n\t- transaction({transaction}) \n\t] to the Bank")
    data = {"card": card, "merchant": merchant, "transaction": transaction}
    sendData_RSA(client_socket_bank, data, PAYMENT_KEY, BANK_KEY)
    
    print("\n=======================================")
    print("waiting for token...\n")
    # get token from the Bank
    data = receiveData_RSA(client_socket_bank,BANK_KEY,PAYMENT_KEY)
    print(f"Received token...")
    print(f"token: \n[ {data} ]")
    return data

# NOTE: App send token to the merchant
# then App receive transaction approval from Merchant
def App_Merchant_2_admin(client_socket_merchant,token):
    
    print("\n=======================================\n")

    # send token to Merchant
    print(f"App: sending token:[ {token} ] to the Merchant")
    sendData_RSA(client_socket_merchant, token, PAYMENT_KEY, MERCHANT_KEY)
    
    print("\n=======================================")
    print("waiting for the transaction approval...\n")

    # receive transaction approval from Merchant
    data = receiveData_RSA(client_socket_merchant,MERCHANT_KEY, PAYMENT_KEY)
    print(f"Received transaction approval...")
    print(f"Transaction approval: \"{data}\"")

    data = "PayApp: OK"
    sendData_RSA(client_socket_merchant, data, PAYMENT_KEY, MERCHANT_KEY)


def checkCard(card):
    cvv = input("Please enter your CVV\n")
    while not cvv.isnumeric() or cvv != card['cvv']:
        incorrect = input(
            "Incorrect CVV, press 1 to enter CVV or 2 to choose another card\n")
        while incorrect != '2' and incorrect != '1':
            incorrect = input(
                "invalid, press 1 to enter CVV or 2 to choose another card\n")
        if incorrect == '1':
            cvv = input("Please enter your CVV\n")
        else:
            card = init()
            cvv = input("Please enter your CVV\n")

    return card, cvv

####################################################################### Main ########################################################################

input("press any key to start...\n")
input("Confirm that Bank and Merchant are running first...\npress any key to start...\n")
input("Sorry, you need to cofirm ^^ \npress any key to start...\n")

client_socket_merchant = requestConnection(MERCHANT_PORT)
print(f"Connecting to the merchant..")

Merchant_Transaction_Data = App_Com_Merchant_1(client_socket_merchant)
merchant = Merchant_Transaction_Data["merchant"]
transaction = Merchant_Transaction_Data["transaction"]

print("\n=======================================")
input("press any key to continue...\n")

card = init()
card, cvv = checkCard(card)
token = {"token": "xczvzxcvzcxv"}

# Now I have merchant data, transaction data and credit card, I'm ready to ask for token


client_socket_bank = requestConnection(BANK_PORT)
print(f"Connecting to the bank")

token = App_Com_Bank(client_socket_bank, card, merchant, transaction)

App_Merchant_2_admin(client_socket_merchant,token)

