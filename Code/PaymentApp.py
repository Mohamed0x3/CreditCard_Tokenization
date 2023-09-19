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
    sleep(0.5)

    data = receiveData_RSA(client_socket_merchant, MERCHANT_KEY, PAYMENT_KEY)
    print(f"Received required data...")
    print(
        f"Merchant info:[ {data['merchant']} ]\n transaction: [ {data['transaction']} ]")

    return data

# NOTE: App send [Card - Merchant - Transaction] data to Bank
#  then App get token from the Bank


def App_Com_Bank(client_socket_bank, card, merchant, transaction):

    print("Connecting to Bank...")
    sleep(0.5)
    # Handshake (App - Bank)
    Handshake_client_Com(client_socket_bank, "App")

    # send [Card - Merchant - Transaction] data to Bank
    print(
        f"App: sending [ \n\t- Card info({card}) \n\t- merchant info({merchant}) \n\t- transaction({transaction}) \n\t] to the Bank")
    sleep(0.5)
    
    data = {"card": card, "merchant": merchant, "transaction": transaction}
    sendData_RSA(client_socket_bank, data, PAYMENT_KEY, BANK_KEY)

    print("\n=======================================")
    print("waiting for token...\n")
    sleep(0.5)
    # get token from the Bank
    data = receiveData_RSA(client_socket_bank, BANK_KEY, PAYMENT_KEY)
    print(f"Received token...")
    print(f"token: \n[ {data} ]")
    return data

# NOTE: App send token to the merchant
# then App receive transaction approval from Merchant


def App_Merchant_2_admin(client_socket_merchant, token):

    print("\n=======================================\n")

    # send token to Merchant
    print(f"App: sending token:[ {token} ] to the Merchant")
    sendData_RSA(client_socket_merchant, token, PAYMENT_KEY, MERCHANT_KEY)

    print("\n=======================================")
    print("waiting for the transaction approval...\n")
    sleep(0.5)

    # receive transaction approval from Merchant
    data = receiveData_RSA(client_socket_merchant, MERCHANT_KEY, PAYMENT_KEY)
    print(f"Received transaction approval...")
    print(f"Transaction approval: \"{data}\"")

    data = "PayApp: OK"
    sendData_RSA(client_socket_merchant, data, PAYMENT_KEY, MERCHANT_KEY)


def checkCard(card):
    cvv = input("Please enter your CVV\n")
    while not cvv.isnumeric() or int(cvv) != int(card['cvv']):
        incorrect = input(
            "Incorrect hhhCVV, press 1 to enter CVV or 2 to choose another card\n")
        while incorrect != '2' and incorrect != '1':
            incorrect = input(
                "invalid, press 1 to enter CVV or 2 to choose another card\n")
        if incorrect == '1':
            cvv = input("Please enter your CVV\n")
        else:
            card = init()
            cvv = input("Please enter your CVV\n")

    return card, cvv

###############################################################################################################
####################################################################### Main ########################################################################
###############################################################################################################


print("Simulation has two modes\n",
      "\t(1) guided simulation \"Guided_Mode = True\"\n",
      "\t(2) normal simulation \"Guided_Mode = False\"\n")

if Guided_Mode:
    print("Current Mode: guided simulation")
else:
    print("Current Mode: normal simulation")
print("if you want to change it: toggle \"Guided_Mode\" value in \"Project_def.py\" file")

print("===================================================\n")

input("press enter key to start...\n")
input("Confirm that Bank and Merchant are running first...\npress enter key to start...\n")
input("Sorry, you need to cofirm ^^ \npress enter key to start...\n")
input("Can you confirm, not just press enter!!\npress enter key to start after you check...\n")


client_socket_merchant = requestConnection(MERCHANT_PORT)
print(f"Connecting to the merchant..")
sleep(0.5)

Merchant_Transaction_Data = App_Com_Merchant_1(client_socket_merchant)
merchant = Merchant_Transaction_Data["merchant"]
transaction = Merchant_Transaction_Data["transaction"]

print("\n=======================================")
input("press enter key to continue...\n")

card = init()
card, cvv = checkCard(card)
token = {"token": "xczvzxcvzcxv"}

# Now I have merchant data, transaction data and credit card, I'm ready to ask for token


client_socket_bank = requestConnection(BANK_PORT)

token = App_Com_Bank(client_socket_bank, card, merchant, transaction)

App_Merchant_2_admin(client_socket_merchant, token)
