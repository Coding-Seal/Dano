import pandas as pd

a = 0.05
data = pd.read_csv("tink.csv")

# v = data.groupby(["code","transaction_amt"]).count().reset_index()
# print(v.code)

v = data.groupby("code").count().reset_index()
v = v.sort_values("transaction_amt")
# print(v)


s = v["transaction_amt"].sum()
for i in range(len(v)+2):
    k = v["transaction_amt"][:i].sum()/s
    if k >= 1 - a:
        print(i)
        break
print(v[179:])
print(7155/s)
