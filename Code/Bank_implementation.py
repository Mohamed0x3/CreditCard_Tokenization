import csv
import hashlib
order = {
    0: "Bank",
    1: "Samsung_Pay",
    2: "Merchant"
}   # (enumerated dictionary) cheap edition
# Be careful of filepaths / how i'm reading keys because it's different

class Bank:

    credit_card_filepath = "C:\\Users\\abdo_\\Desktop\\credit_cards.csv"   # credit_card filepath we can change it
    tokenized_cards_filepath = "C:\\Users\\abdo_\\Desktop\\token.csv"      # we can ignore it
    public_key_path = "C:\\Users\\abdo_\\Desktop\\public_keys.txt"
    credit_card_list = []   # to convert from csv file to list
    tokenized_list = []     # to store tokens of cards
    private_key = ""        # will be written in phase 2
    public_key = []         # list to store public_keys

    def __init__(self):
        with open(self.credit_card_filepath, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)   # i don't know why but here when using delimiter='\t' it gives error
            for row in csv_reader:
                self.credit_card_list.append(row)
                # i made a list format = [{'person': , 'card_num': ,'CVV':,'balance':}]

        with open(self.public_key_path, 'r') as file:
            # assume that the order is bank , samsung_pay , merchant
            i = 0
            for line in file:
                self.public_key.append({order[i]: int(line)})
                i += 1
        with open(self.tokenized_cards_filepath, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter="\t")
            for row in csv_reader:
                self.tokenized_list.append(row)

    def update_db(self):
        with open(self.credit_card_filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.credit_card_list[0].keys())
            writer.writeheader()
            for i in self.credit_card_list:
                writer.writerow(i)

    # my idea is to make the token = (credit_card_num + public_key of merchant +cvv) then hash it using sha_512
    # so for same credit_card the public_key make tokens different
    def transact(self, token, public_key, cvv, product_price):
        for i in self.credit_card_list:
            temp = i["card_num"]+cvv+str(public_key)
            temp_hash = hashlib.sha512()
            temp_hash.update(temp.encode('utf-8'))
            result = temp_hash.hexdigest()
            if result == token:
                # i found it so check on balance to see if i can make transaction
                if int(i['Balance']) > product_price:
                    new_balance = int(i['Balance']) - product_price
                    i['Balance'] = new_balance          # update the current balance for this run
                    self.update_db()
                    print("Successful Transaction")
                else:
                    print("No money, Unsuccessful Transaction")
            break

    def tokenize(self, credit_card, cvv, public_key):
        for i in self.credit_card_list:
            if credit_card == i["card_num"] and cvv == i["CVV"]:     # check if the card is present
                token = hashlib.sha512()    # create sha512 object
                token.update((credit_card+cvv+str(public_key)).encode('utf-8'))
                # update is used to concatenate string inside sha object so when i call digest it hash the data
                result = token.hexdigest()                               # hashing and put result in result
                self.tokenized_list.append(result)           # put it in the list for the current run-time
                with open(self.tokenized_cards_filepath, 'a', newline='')as csvfile:
                    # write it in csv file for future run-times
                    writer = csv.writer(csvfile)
                    writer.writerow({result})
                print("successful tokenization".title())
                return 0
        print("unsuccessful tokenization, The card given or cvv is wrong".title())



mybank = Bank()
# print(mybank.credit_card_list)
# mybank.tokenize('123456781',"321",1)
#mybank.transact('b234ed3597ee338efdce2b7809e5ba16d2528d4f8c0d1e1ce9f06e9b16548f83595667fd478c58a98f7a3a688912aa3ce56c76db7b04cf45735a08a1b79c6f8f',  1,'321',1000)
# print(mybank.tokenized_list)