<div align = "center">
<h1>Credit Card Tokenization <br/> Simulation</h1>
  
![tokenization-cover](https://i.imgur.com/bK4kf5A.jpg)

![Used lang](https://img.shields.io/badge/Python-Most_used-4584b6)

An educational project for Cybersecurity training course taken during 2023 summer.

</div>

## ❕ Problem Definition

It's critical to have a secure system that totally meets the CIA triad (Confidentiality, Integrity, and Availability).
Credit card tokenization process is more secure than using Card info(username, password, etc..) with Merchant.

Note that: If card info is leaked(Hacker got it 😱), you will be broke 😭

| ![Donald with money](https://i.imgur.com/YbLV5Rv.gif) | ![right-wrong](https://i.imgur.com/iZ3wUlO.jpg) | ![Donald with money](https://i.imgur.com/vbxLfbV.gif) |
| ----------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------- |

<br/>

Our project is a process simulation to (apply / help understande) the credit card tokenization process between Tokenization System (e.g. Bank or Credit Card Provider), Merchant, and End-User Program (e.g. Samsung pay) by:

- Making transaction more secure.
- Less share credit card data.
- Making transaction data useless for an outside person (e.g. Hacker).

## ➡️ Modules and Roles

### PaymetApp (card owner)

- Buy products from merchant
- Ask bank to do tokenization for tokens to do transactions

### Bank (card provider)

- Do tokenization
- Do transaction

### Merchant

- Ask paymentApp for a token to do the transactions
- Ask Bank to do the transaction

## ➡️ Tokenization Cycle

<div align = "center">
  
  ![Tokenization cycle](https://i.imgur.com/UZVD72F.png)
</div>

## ➡️ Tokenization Sequence Diagram

```mermaid

sequenceDiagram

autonumber

rect rgb(191, 223, 255)

PaymentApp ->> Merchant: Get Connection

Merchant --> PaymentApp: handshake

Merchant -->> PaymentApp: Data (Merchant data, Transaction data)

Note over Merchant: Waiting for token...

end

Note over PaymentApp: App asks user about <br/> credit card info

rect rgb(200, 150, 255)

PaymentApp ->> Bank: Get Connection

Bank --> PaymentApp: handshake

PaymentApp -->> Bank: Data (Credit all data, Merchant data, Transaction data)

Note over Bank: Bank validate Data

Note over PaymentApp: Waiting for token...

Note over Bank: If False

Bank -->> PaymentApp: Failure Message

Note over Bank: If True

Bank -->> PaymentApp: Token

end



rect rgb(191, 223, 255)

PaymentApp -->> Merchant: Token

Note over PaymentApp: Waiting for transaction <br/> approval...

end



rect rgb(207, 70, 71)

Merchant ->> Bank: Get Connection

Bank --> Merchant: handshake


Merchant -->> Bank: Data (Token, Merchant data, Transaction data)

Note over Bank: Bank validate Data


Note over Merchant: Waiting for transaction <br/> approval...

Note over Bank: If False

Bank -->> Merchant: Failure Message

Note over Bank: If True

Bank -->> Merchant: "Successful Transaction"

end

Note over Merchant: If False

rect rgb(191, 223, 255)

Merchant -->> PaymentApp: Failure Message

end

Note over Merchant,Bank: If True

rect rgb(191, 223, 255)

Merchant -->> PaymentApp: "Successful Transaction"

end

rect rgb(200, 150, 255)

Bank -->> PaymentApp: Data (Last Transaction info, Credit info)

end

```

## ➡️ Simulation Types

- Normal/Hacker Mode
  - Normal Mode: simulate normal transaction.
  - Hacker Mode: simulate hacker got all transaction data and communicate with bank to do unauthorized transaction.
- Guided/Non-Guided Mode
  - Guided Mode: to send any communication message, it will ask for pressing Enter first.
  - Non-Guided Mode: simulation is done instantly.

## 🎬 Video Demo

<div align=center>

<a href="https://vimeo.com/870020720" target="_blank">
  <img src="https://i.imgur.com/MgwU3c7.jpg"/>
</a>

</div>

## 🛠️ How to Run

<!-- Steps! -->

- 🔨 Clone the repository by pressing the green button.
- 🔨 To run Normal Mode:
  - [3 times] Once in the folder, type CMD in the address bar.
    - run commands(one in each):
      - `py Code/Bank.py`
      - `py Code/Merchant.py`
      - `py Code/PaymentApp.py`
- 🔨 To run Hacker Mode:
  - [2 times] Once in the folder, type CMD in the address bar.
    - run commands(one in each):
      - `py Code/Bank.py`
      - `py Code/Merchant.py`

## 👨‍💻 Technical Stuff

- Communication between modules(PaymentApp, Bank, Merchant) is done using Sockets.
- Communication is secure. It is encrypted and decrypted using AES with public/private keys.

## ➡️ More Info

- <a href="https://youtu.be/dQy-bGoQYSM?si=7-v3PtfHRDpM80tF" target="_blank"> Visa and tokens: multiple paths to payment security </a>
- <a href="https://youtu.be/iVeenkfa-0s?si=sUwwH3hJW7csApOH" target="_blank"> What Is Tokenization? </a>
- <a href="CS_Credit Card tokenization_Project Proposal.docx" target="_blank"> Project Document </a>
