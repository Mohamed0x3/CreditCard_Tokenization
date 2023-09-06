from modules.Project_def import *
from modules.Payment_def import *

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

card = "?"
merchant = "?"
transaction = "?"

token = {"token": "xczvzxcvzcxv"}

# ======================== THREAD 1

# PayApp act as a client with the Merchant (TODO Thread - HEMLY)
client_socket = requestConnection(MERCHANT_PORT)
data = receiveData(client_socket)
merchant = data["merchant"]
print(f"{data}")
# TODO Print available transactions
# select wanted transaction (TODO Ask user - HELMY)
data["transaction number"] = 1
transaction = data["transactions"][0]
# select credit card (TODO - HEMLY)
card = "?"

# TODO - HELMY (This thread wait for token from "THREAD 2")

data["token"] = token["token"]
sendData(client_socket, data)

data["approved"] = False
sendData(client_socket, data)
data = receiveData(client_socket)

if data["approved"] is False:
    print(f"ERROR")  # This will not happen!!


# ======================== THREAD 2

# PayApp act as a client with the bank
client_socket = requestConnection(BANK_PORT)
data = receiveData(client_socket)
print(f"1 {data}")
data["message"] = "app"
sendData(client_socket, data)
print(f"test {data}")
data = receiveData(client_socket)
while True:
    data["card"] = card
    data["merchant"] = merchant
    data["transaction"] = transaction
    sendData(client_socket, data)
    data = receiveData(client_socket)
    if data["flag"] is False:
        print(f"wrong card data... try again")
        continue
    token = {"merchant": merchant, "token": data["token"]}
    break
