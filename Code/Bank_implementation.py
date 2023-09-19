import hashlib
import pandas as pd
import pathlib
import random

order = {
    0: "Bank",
    1: "Samsung_Pay",
    2: "Merchant"
}   # (enumerated dictionary) cheap edition
# Be careful of filepaths / how i'm reading keys because it's different
BANK_CARDS_DB_PATH = pathlib.Path("./tstDB/credit_cards.csv")
BANK_TOKENS_DB_PATH = pathlib.Path("./tstDB/token.csv")


class Bank:

    # credit_card filepath we can change it
    credit_card_filepath = "C:\\Users\\abdo_\\Desktop\\credit_cards.csv"
    tokenized_cards_filepath = "C:\\Users\\abdo_\\Desktop\\token.csv"      # we can ignore it
    public_key_path = "C:\\Users\\abdo_\\Desktop\\public_keys.txt"
    # credit_card_list = []   # to convert from csv file to list
    tokenized_list = []     # to store tokens of cards
    # private_key = ""        # will be written in phase 2
    # public_key = []         # list to store public_keys

    def __init__(self):
        self.credit_card_df = pd.read_csv(BANK_CARDS_DB_PATH)

        self.tokens_df = pd.read_csv(BANK_TOKENS_DB_PATH)
        # self.tokenized_list = self.tokens_df["token"]

    # my idea is to make the token = (credit_card_num + public_key of merchant +cvv) then hash it using sha_512
    # so for same credit_card the public_key make tokens different
    def transact(self, token, product_price, merchant_id, transactio_id):

        for i, row in zip(range(len(self.credit_card_df)), self.credit_card_df.values):
            temp = str(row[1])+str(row[4])+str(merchant_id)+str(transactio_id)
            temp_hash = hashlib.sha512()
            temp_hash.update(temp.encode('utf-8'))
            result = temp_hash.hexdigest()

            if result == token:
                response = ""
                # i found it so check on balance to see if i can make transaction
                if int(row[5]) >= product_price:
                    new_balance = int(row[5]) - product_price
                    # update the current balance for this run
                    row[5] = new_balance
                    self.credit_card_df.loc[i] = row
                    self.credit_card_df.to_csv(BANK_CARDS_DB_PATH, index=False)
                    print("Successful Transaction")
                    print(
                        "we assume that credits were sent to merchant bank account sucessfully")

                    response = "Successful Transaction"
                else:
                    print("No money, Unsuccessful Transaction")
                    response = "No money, Unsuccessful Transaction"

                filter = self.tokens_df[self.tokens_df["token"] == token]
                self.tokens_df = self.tokens_df.drop(filter.index)
                self.tokens_df.to_csv(BANK_TOKENS_DB_PATH, index=False)
                return response

        print("Wrong token")
        return "Wrong token"

    def addToken(self, token, merchant_id, transaction_id):
        newDF = pd.DataFrame({"token": token, "merchant_id": merchant_id, "transaction_id": transaction_id}, index=[
                             len(self.tokenized_list)])
        self.tokens_df = pd.concat([self.tokens_df, newDF], axis=0)
        self.tokens_df.to_csv(BANK_TOKENS_DB_PATH, index=False)
        self.tokenized_list = self.tokens_df["token"]

    def tokenize(self, credit_card, cvv, merchant_id, transaction_id):
        
        # check if the card is present
        filter = self.credit_card_df[(self.credit_card_df["number"]
                                     == credit_card) & (self.credit_card_df["cvv"] == cvv)]
        print(filter)
        if len(filter) == 0:
            print("unsuccessful tokenization, The card given or cvv is wrong".title())
            return -1
        else:
            token = hashlib.sha512()    # create sha512 object
            token.update((str(credit_card)+str(cvv) +
                         str(merchant_id)+str(transaction_id)).encode('utf-8'))
            # update is used to concatenate string inside sha object so when i call digest it hash the data
            # hashing and put result in result
            result = token.hexdigest()

            self.addToken(result, merchant_id, transaction_id)
            print("successful tokenization".title())

            return result


mybank = Bank()
# print(mybank.tokens_df)
# mybank.tokenize(123456781,321,121212)
# print(mybank.tokens_df)
# print(mybank.credit_card_df)
# mybank.transact("588ef73015491751c58f14480273d3357a53b0aec2c2152fe7fef598eddd5e28f663f5caeeda1a02a9ae555209ffca993a35d8b4e7724ce5a758cc2e5dd4feb1", 8500, 121212)
# print(mybank.credit_card_df)
