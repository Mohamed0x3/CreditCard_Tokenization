from modules.Project_def import *
from modules.Payment_def import *

# This function ends with (app get token from the bank)
def App_Bank(client_socket_bank, card, merchant, transaction):

    data = {"card": card, "merchant": merchant, "transaction": transaction}

    payload = json.dumps(data).encode()
    encrypted = encrypt(payload, BANK_KEY.publickey())
    sendData(client_socket_bank, encrypted)
    print("sending encrypted data to bank, waiting for token")
    data = receiveData(client_socket_bank)
    print(f"Received encrypted token: \n{data}")

    decrypted=decrypt(ast.literal_eval(str(data)),PAYMENT_KEY)
    print(f"Decrypted token:\n{decrypted}")
    return decrypted

def App_Merchant_1_admin(client_socket_merchant):
    # "Merchant say \"Hello\" to App"
    data = receiveData(client_socket_merchant)
    print(data)
    data = "App reply \"Hello\" to Merchant"
    print("replying to the merchant to confirm connection..")
    sendData(client_socket_merchant, data)
    print("waiting for merchant info..")
    data = receiveData(client_socket_merchant)
    print(f"received encrypted data from the merchant:\n{data}")
    
    decrypted = decrypt(ast.literal_eval(str(data)), PAYMENT_KEY)
    data = json.loads(decrypted.decode())
    print(f"Merchant & Transaction Data after dectyption:\n {data}")
    return data


def App_Bank_admin(client_socket_bank, card, merchant, transaction):
    data = receiveData(client_socket_bank)  # "Bank say \"Hello\" to App"
    print(data)
    print("sending reply signal to bank")
    data = "App reply \"Hello\" to Bank"
    sendData(client_socket_bank, data)
    return App_Bank(client_socket_bank, card, merchant, transaction)


def App_Merchant_2_admin(client_socket_merchant,token):
    # data = "App give \"token\" to Merchant"
    print("sending encrypted token to the merchant")
    enToken=encrypt(token,MERCHANT_KEY.publickey())
    sendData(client_socket_merchant, enToken)
    # "\"Transaction is ok\" Merchant and App are Friends?"
    print("waiting for confirmation from merchant")
    data = receiveData(client_socket_merchant)
    print(data)
    data = "Merchant and App are Friends?... YES"
    sendData(client_socket_merchant, data)


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

####################################################################### Samir ########################################################################
# Steps:


# TODO send request to the merchant to get his info and transaction info (this is done when scanning barcode or using nfc)--->done
# select credit card---->done
card = init()
# Not sure if this step is done by the payment app or it should be done by the bank
card, cvv = checkCard(card)
# TODO send the data of merchant and transaction & credit card with cvv (input when select credit card) to the bank to get a token
# TODO send the token to the merchant
# TODO the merchant should send the token to the bank and if it's correct the transaction will be done between the merchant account & user account
# TODO when merchant receive acknowledge that transaction was done successfully it should send signal to payment app
# TODO the app prints info that transaction was done

token = {"token": "xczvzxcvzcxv"}

# ======================== THREAD 1

client_socket_merchant = requestConnection(MERCHANT_PORT)
print(f"Connecting to the merchant..")

# merchant,transaction = App_Merchant_1(client_socket_merchant)
Merchant_Transaction_Data = App_Merchant_1_admin(client_socket_merchant)
merchant = Merchant_Transaction_Data["merchant"]
transaction = Merchant_Transaction_Data["transaction"]
# Now I have merchant data, transaction data and credit card, I'm ready to ask for token


client_socket_bank = requestConnection(BANK_PORT)
print(f"Connecting to the bank")


token = App_Bank_admin(client_socket_bank, card, merchant, transaction)

App_Merchant_2_admin(client_socket_merchant,token)

