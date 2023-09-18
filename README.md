# CreditCard_Tokenization

This project proposes the development of a credit card tokenization system and simulates the cycle of paying with a phone. The system will consist of three programs: End-User Program (e.g. Samsung Pay), Tokenization System (e.g. Bank or Credit Card Provider) and Merchant.

## Sequence Diagram

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

Bank -->> PaymentApp: ?

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
