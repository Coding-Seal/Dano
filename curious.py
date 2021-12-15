import pandas as pd

data = pd.read_csv("final.csv", sep=";")

flag = dict(online=1, offline=0)
data["online_transaction_flg"] = data["online_transaction_flg"].replace(flag)
data = data.reset_index()

cust = data[["customer_id", "online_transaction_flg"]]
online = cust.groupby("customer_id").all("online_transaction_flg")
online = online.reset_index()

# print(online)
# offline = cust.groupby("customer_id").all("online_transaction_flg", skipna=False)

count = cust.groupby("customer_id").count()
count = count.reset_index()
# print(count > 24)

# print(count)
active_online = cust[(count > 24) | online]
active_online.reset_index()
print(active_online)
