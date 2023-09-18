from modules.Project_def import *
from modules.Payment_def import *

# NOTE: App do handshake with the Merchant
#  then App get [Merchant - Transaction] data
def App_Com_Merchant_1(client_socket_merchant):

    # Handshake (Bank - Merchant)
    data = receiveData_RSA(client_socket_merchant,MERCHANT_KEY, PAYMENT_KEY) # "Merchant say \"Hello\" to App"
    print(data)
    data = "App reply \"Hello\" to Merchant"
    print("replying to the merchant to confirm connection..")
    sendData_RSA(client_socket_merchant, data,PAYMENT_KEY,MERCHANT_KEY)

    # receive [merchant - transaction - token] data from Merchant
    print("waiting for merchant info..")
    data = receiveData_RSA(client_socket_merchant,MERCHANT_KEY, PAYMENT_KEY)
    print(f"Merchant & Transaction Data after dectyption:\n {data}")
    
    return data

# NOTE: App send [Card - Merchant - Transaction] data to Bank
#  then App get token from the Bank
def App_Com_Bank(client_socket_bank, card, merchant, transaction):
    
    data = receiveData_RSA(client_socket_bank,BANK_KEY,PAYMENT_KEY)  # "Bank say \"Hello\" to App"
    print(data)
    print("sending reply signal to bank")
    data = "App reply \"Hello\" to Bank"
    sendData_RSA(client_socket_bank, data,PAYMENT_KEY,BANK_KEY)
    
    # send [Card - Merchant - Transaction] data to Bank
    data = {"card": card, "merchant": merchant, "transaction": transaction}
    sendData_RSA(client_socket_bank, data, PAYMENT_KEY, BANK_KEY)
    print("sending encrypted data to bank, waiting for token")
    
    # get token from the Bank
    data = receiveData_RSA(client_socket_bank,BANK_KEY,PAYMENT_KEY)
    print(f"Decrypted token:\n{data}")

    return data

# NOTE: App send token to the merchant
# then App receive transaction approval from Merchant
def App_Merchant_2_admin(client_socket_merchant,token):
    
    # send token to Merchant
    print("sending encrypted token to the merchant")
    sendData_RSA(client_socket_merchant, token, PAYMENT_KEY, MERCHANT_KEY)
    
    # receive transaction approval from Merchant
    print("waiting for confirmation from merchant")
    data = receiveData_RSA(client_socket_merchant,MERCHANT_KEY, PAYMENT_KEY)
    print(data)

    data = "PayApp: OK"
    sendData_RSA(client_socket_merchant, data, PAYMENT_KEY, MERCHANT_KEY)


def checkCard(card):
    cvv = input("Please enter your CVV\n")
    while cvv != card['cvv']:
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

card = init()
card, cvv = checkCard(card)
token = {"token": "xczvzxcvzcxv"}

client_socket_merchant = requestConnection(MERCHANT_PORT)
print(f"Connecting to the merchant..")

Merchant_Transaction_Data = App_Com_Merchant_1(client_socket_merchant)
merchant = Merchant_Transaction_Data["merchant"]
transaction = Merchant_Transaction_Data["transaction"]
# Now I have merchant data, transaction data and credit card, I'm ready to ask for token

client_socket_bank = requestConnection(BANK_PORT)
print(f"Connecting to the bank")

token = App_Com_Bank(client_socket_bank, card, merchant, transaction)

App_Merchant_2_admin(client_socket_merchant,token)

