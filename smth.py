import numpy as np
import plotly.express as px
import pandas as pd

data_i = pd.read_csv("tink.csv")
m_data = pd.read_csv('modified.csv')
data = pd.read_csv('modified.csv')
mcc = pd.read_csv("mcc_code.csv", sep=";", encoding="Windows-1251")
mcc_list = [5814,
            9402,
            7230,
            5200,
            5311,
            7999,
            9399,
            5651,
            4131,
            5993,
            5921,
            3423,
            5541,
            7512,
            5912,
            5812,
            5499,
            4111,
            4121,
            5814,
            5411,
7832
            ]

our_code = data['code'].isin(mcc_list)
data = data[our_code]
# # print(data[data["code"] == "Авиалинии, авиакомпании"][["transaction_amt", "day_time"]])
# i = 0
# for code in data["code"].unique():
#     if len(data[data["code"] == code]) < 100:
#         i += 1
#         #
#         # if data[data["code"] == code]["transaction_amt"].sum() >= 200000:
#         #     print(code, data[data["code"] == code]["transaction_amt"].sum())
#         data = data[data['code'] != code]

# print(data[data["code"]=="Аэрофлот"][["transaction_amt", "day_time","customer_id"]].reset_index())
# print(i)
#
mcc = dict(zip(mcc["mcc"], mcc["значение mcc"]))

data["code"] = data["code"].replace(mcc)

data = data.reset_index()
data = data[["online_transaction_flg", "code", "category", "transaction_amt",
             "customer_id", "day_time", "day_of_week", "time_of_day"]]

data.to_csv("final.csv", sep=";")
# print(len(data["code"].unique()))
# print(len(m_data["code"].unique()))
#
# print(len(data["code"].unique()))

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
