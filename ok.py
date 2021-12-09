import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go
from scipy import stats
from baskets import kras

data = pd.read_csv('modified.csv')
mcc = pd.read_csv("mcc_code.csv", sep=";", encoding="Windows-1251")
data["unused"] = np.zeros(len(data["category"]), dtype="bool")

mcc = dict(zip(mcc["mcc"], mcc["значение mcc"]))

data["code"] = data["code"].replace(mcc)
for code in data["code"].unique():
    if len(data[data["code"] == code]) < 10:
        data["unused"] |= data["code"] == code

data = data.reset_index()
data = data[["online_transaction_flg", "code", "category", "transaction_amt", "customer_id", "day_time", "unused"]]

for mcc in data.code.unique():
    online = data[data["online_transaction_flg"] == "online"]
    offline = data[data["online_transaction_flg"] == "offline"]
    online = online[(np.abs(stats.zscore(data["transaction_amt"])) < 3)]
    offline = offline[(np.abs(stats.zscore(data["transaction_amt"])) < 3)]
