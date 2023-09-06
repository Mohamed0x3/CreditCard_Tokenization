# CreditCard_Tokenization
This project proposes the development of a credit card tokenization system and simulates the cycle of paying with a phone. The system will consist of three programs: End-User Program (e.g. Samsung Pay), Tokenization System (e.g. Bank or Credit Card Provider) and Merchant.

## Sequence Diagram
```mermaid
sequenceDiagram
rect rgb(191, 223, 255)
PaymentApp ->> Merchant: Get Connection
Merchant -->> PaymentApp: Here my products
PaymentApp-->> Merchant: I want product x
Merchant -->> PaymentApp: Data (Merchant data, Transaction data)
end
Note over PaymentApp: App asks user if <br/> he want to confirm <br/> this transaction <br/> & Ask him for<br/> credit card!

rect rgb(200, 150, 255)
PaymentApp ->> Bank: Get Connection
Bank -->> PaymentApp: App or Merchant?
PaymentApp -->> Bank: App
Bank -->> PaymentApp: Data?
PaymentApp -->> Bank: Data (Credit all data, Merchant data, Transaction data)
Note over Bank: Bank validate Data
Note over Bank: If False
Note over Bank: If True
Bank -->> PaymentApp: Token
end

rect rgb(191, 223, 255)
PaymentApp -->> Merchant: Token
end

rect rgb(188, 62, 62)
Merchant ->> Bank: Get Connection
Bank -->> Merchant: App or Merchant?
Merchant -->> Bank: Merchant
Bank -->> Merchant: Data?
Merchant -->> Bank: Data (Token, Merchant data, Transaction data)
Note over Bank: Bank validate Data
Note over Bank: If False
Note over Bank: If True
Bank -->> Merchant: Transcation Flag (True = happened / False = failed)
end
Note over Merchant: If False
rect rgb(191, 223, 255)
Merchant -->> PaymentApp: Transcation Flag (False = failed)
end
Note over Merchant,Bank: If True
rect rgb(191, 223, 255)
Merchant -->> PaymentApp: Transcation Flag (True = happened)
end
rect rgb(200, 150, 255)
Bank -->> PaymentApp: Data (Last Transaction info, Credit info)
end
```
