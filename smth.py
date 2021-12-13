import numpy as np
import plotly.express as px
import pandas as pd
data_i = pd.read_csv("tink.csv")
m_data = pd.read_csv('modified.csv')
data = pd.read_csv('modified.csv')
mcc = pd.read_csv("mcc_code.csv", sep=";", encoding="Windows-1251")


mcc = dict(zip(mcc["mcc"], mcc["значение mcc"]))

data["code"] = data["code"].replace(mcc)
# print(data[data["code"] == "Авиалинии, авиакомпании"][["transaction_amt", "day_time"]])
# i = 0
for code in data["code"].unique():
    if len(data[data["code"] == code]) < 20:

        # i+=1
        #
        # if data[data["code"] == code]["transaction_amt"].sum() >= 200000:
        #     print(code, data[data["code"] == code]["transaction_amt"].sum())
        data = data[data['code'] != code]

# print(data[data["code"]=="Аэрофлот"][["transaction_amt", "day_time","customer_id"]].reset_index())
print(i)
#
data = data.reset_index()
data = data[["online_transaction_flg", "code", "category", "transaction_amt", "customer_id", "day_time"]]
# data.to_csv("final.csv",sep = ";")
print(len(data_i["code"].unique()))
print(len(m_data["code"].unique()))

print(len(data["code"].unique()))

# week = ("Понедельник ", "Вторник ", "Среда ", "Четверг ", "Пятница ", "Суббота ", "Воскресенье ")
#
# data["day_time"]=data["day_of_week"]
# for i in range(1, 8):
#     data["day_time"]= data["day_time"].replace(i, week[i-1])
# data["online_transaction_flg"]= data["online_transaction_flg"].replace(1,"online")
# data["online_transaction_flg"]= data["online_transaction_flg"].replace(0,"offline")
#
# data["day_time"] += data["time_of_day"]
#
# data.to_csv("modified.csv")
#
# print(data)
