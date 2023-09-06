import pandas as pd
import pathlib

paymentAppDBPath = pathlib.Path("./tstDB/paymentAppDB.csv")

df=pd.DataFrame({"name": ['Samir','Taher','Hefney','Helmy'], "number": ['1234567891234567','7654321987654321','1122334455667788','8877665544332211'], "exp_month": [9,7,5,12],
             "exp_year": [2025,2024,2026,2025], "cvv": [123,456,789,321]})


df.to_csv(paymentAppDBPath,index=False)

print(pd.read_csv(paymentAppDBPath).head(5))


