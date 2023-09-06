# Note: THIS FILE IS DUMMY
#       you can update it or replace it

import pandas as pd
import pathlib
import numpy as np


PAYMENT_APP_DB_PATH = pathlib.Path("./tstDB/paymentAppDB.csv")


def getCreditCridintioals():
    name = input(f"Enter credit card owner's name: ")
    number = input(f"Enter credit card number: ")
    exp_month = input(f"Enter credit card expirey month: ")
    exp_year = input(f"Enter credit card expirey year: ")
    cvv = input(f"Enter credit card Password: ")

    return {
        "name": name,
        "number": number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvv": cvv,
    }


def addNewCreditCard():
    credit_card = getCreditCridintioals()
    # add card data to the app database (NOT INCLUDING THE PASSWORD) --------------------------> Not sure about storing cvv
    cardsDB = pd.read_csv(PAYMENT_APP_DB_PATH)
    newDF = pd.DataFrame(credit_card,index=[len(cardsDB)])
    print(newDF)
    cardsDB = pd.concat([cardsDB, newDF], axis=0)
    cardsDB.to_csv(PAYMENT_APP_DB_PATH, index=False)
    return credit_card


def printCard(i, card):
    print(
        f"Card {i} Detailes: \n\n"
        f"\tcard owener's name: {card['name']}\n"
        f"\tcard number: {card['number']}\n"
        f"\tcard expiration date MM/YY: {card['exp_month']}/{card['exp_year']} \n"
    )


def printAvaliableCards():
    # get card from database
    cardsDB = pd.read_csv(PAYMENT_APP_DB_PATH)
    print()
    for card, i in zip(cardsDB.values, range(len(cardsDB.values))):
        print('-----------------------------------------------------------------------')
        printCard(i, dict(zip(cardsDB.columns, card)))

    return len(cardsDB.values), cardsDB.values


def selectCreditCard():
    cardsLen, values = printAvaliableCards()
    if cardsLen == 0:
        return addNewCreditCard(), cardsLen
    print(
        f"Choose from your cards [{0}-{cardsLen-1}] or press (A/a) to add new one")
    d = input("Waiting for your decision...")

    while (d != 'A' and d != 'a' and not d.isnumeric()) or (d.isnumeric() and (int(d) < 0 or int(d) >= cardsLen)):
        print("Invalid input, choose from your cards or press (A/a) to add new one")
        d = input("Waiting for your decision...")

    if d == 'A' or d == 'a':
        return addNewCreditCard(), cardsLen
    else:
        return {
            'name': values[int(d), 0],
            "number": values[int(d), 1],
            "exp_month": values[int(d), 2],
            "exp_year": values[int(d), 3],
            "cvv": values[int(d), 4],
        }, int(d)


a, b = selectCreditCard()
printCard(b, a)
