# Note: THIS FILE IS DUMMY
#       you can update it or replace it


def getCreditCridintioals():
    name = input(f"Enter credit card owner's name: ")
    number = input(f"Enter credit card number: ")
    exp_month = input(f"Enter credit card expirey month: ")
    exp_year = input(f"Enter credit card expirey year: ")
    password = input(f"Enter credit card Password: ")

    return {
        "name": name,
        "number": number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "password": password,
    }


def addNewCreditCard():
    credit_card = getCreditCridintioals
    # add card data to the app database (NOT INCLUDING THE PASSWORD)


def printCard(card):
    print(
        f"Card Detailes: \n"
        f"\tcard owener's name: {card['name']}\n"
        f"\tcard number: {card['number']}\n"
        f"\tcard expiration date MM/YY: {card['exp_month']}/{card['exp_year']} \n"
    )


def printAvaliableCards():
    # get card from database
    for card in db:
        printCard(card)
