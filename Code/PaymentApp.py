from modules.Project_def import *
from modules.Payment_def import *


# TODO (SAMIR \ TAHER|HELMY) => This function will end with (app have merchant and transaction data)
def App_Merchant_1 (client_socket_merchant):
    # PayApp act as a client with the Merchant (TODO Thread - HEMLY)
    data = receiveData(client_socket_merchant)
    print(f"Recived Data from merchant: ")
    merchant = data["merchant"]
    print(f"\t{data}")
    # TODO Print available transactions
    # select wanted transaction (TODO Ask user - HELMY)
    data["transaction number"] = 1
    transaction = data["transactions"][0]
    # select credit card (TODO - HEMLY)
    card = "?"
    return merchant,transaction
# TODO (SAMIR \ HEFNEY) => This function will end with (app get token from the bank)
def App_Bank (BANK_PORT,card,merchant,transaction):
    # PayApp act as a client with the bank
    client_socket_bank = requestConnection(BANK_PORT)
    data = receiveData(client_socket_bank)
    print(f"1 {data}")
    data["message"] = "app"
    sendData(client_socket_bank, data)
    print(f"test {data}")
    data = receiveData(client_socket_bank)
    while True:
        data["card"] = card
        data["merchant"] = merchant
        data["transaction"] = transaction
        sendData(client_socket_bank, data)
        data = receiveData(client_socket_bank)
        if data["flag"] is False:
            print(f"wrong card data... try again")
            continue
        token = {"merchant": merchant, "token": data["token"]}
        return token
# TODO (SAMIR \ TAHER|HELMY) => This function will end with (app give token to merchant and do transaction)
def App_Merchant_2(client_socket_merchant,token):
    data["token"] = token["token"]
    sendData(client_socket_merchant, data)

    data["approved"] = False
    sendData(client_socket_merchant, data)
    data = receiveData(client_socket_merchant)

    if data["approved"] is False:
        print(f"ERROR")  # This will not happen!!

def App_Merchant_1_admin(client_socket_merchant):
    data = receiveData(client_socket_merchant) #"Merchant say \"Hello\" to App"
    print(data)
    data = "App reply \"Hello\" to Merchant"
    sendData(client_socket_merchant, data)
def App_Bank_admin(BANK_PORT):
    client_socket_bank = requestConnection(BANK_PORT)
    print(f"Connected to the bank")
    data = receiveData(client_socket_bank) #"Bank say \"Hello\" to App"
    print(data)
    data = "App reply \"Hello\" to Bank"
    sendData(client_socket_bank, data)
    data = receiveData(client_socket_bank) #"Bank give \"token\" to App"
    print(data)
def App_Merchant_2_admin(client_socket_merchant):
    data = "App give \"token\" to Merchant"
    sendData(client_socket_merchant, data)
    data = receiveData(client_socket_merchant) #"\"Transaction is ok\" Merchant and App are Friends?"
    print(data)
    data = "Merchant and App are Friends?... YES"
    sendData(client_socket_merchant, data)
####################################################################### Samir ########################################################################


#TODO send request to the merchant to get his info and transaction info (this is done when scanning barcode or using nfc)
#select credit card
card = init()
#TODO send the data of merchant & credit card with cvv (input when select credit card) to the bank to get a token
#TODO send the token to the merchant
#TODO the merchant should send the token to the bank and if it's correct the transaction will be done between the merchant account & user account
#TODO when merchant receive acknowledge that transaction was done successfully it should send signal to payment app
#TODO the app prints info that transaction was done

######################################################################################################################################################

# Note: Next Comments are related to modules.Payment_def
#       you can update it or replace it

# db = "?"  ------------------> csv for testing
# card = getCreditCridintioals()
# card_without_pass = {
#     "name": card["name"],
#     "number": card["number"],
#     "exp_month": card["exp_month"],
#     "exp_year": card["exp_year"],
#     "password": card["password"],
# }
# printCard(card_without_pass)
# db.add(card_without_pass)

# get merchant data
# send card data with merchant name to the bank

#card = "?"----------------------->done
merchant = "?"
transaction = "?"

token = {"token": "xczvzxcvzcxv"}

# ======================== THREAD 1

client_socket_merchant = requestConnection(MERCHANT_PORT)
print(f"Connected to the merchant")

# merchant,transaction = App_Merchant_1(client_socket_merchant)
App_Merchant_1_admin(client_socket_merchant)

# TODO - HELMY (This thread wait for token from "THREAD 2")
# ======================== THREAD 2 (Start)

# token = App_Bank(BANK_PORT,card,merchant,transaction)
App_Bank_admin(BANK_PORT)

# ======================== THREAD 2 (End)

# App_Merchant_2(client_socket_merchant,token)
App_Merchant_2_admin(client_socket_merchant)
