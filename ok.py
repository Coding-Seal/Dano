import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go
from scipy import stats
from baskets import kras
from scipy.interpolate import Akima1DInterpolator as Akima

data = pd.read_csv("tink.csv", sep=",")

smth = ["Авиабилеты", "Автоуслуги", "Аптеки",
        "Аренда авто", "Госсборы", "Дом/Ремонт",
        "Красота", "Медицинские услуги", "Одежда/Обувь",
        "Рестораны", "Сервисные услуги", "Супермаркеты",
        "Топливо", "Транспорт", "Фаст Фуд"]

print("category     offline      online")

for cat in smth:
    category = data[data["category"] == cat]
    on = category[category["online_transaction_flg"] == 1]["transaction_amt"].sum()
    off = category[category["online_transaction_flg"] == 0]["transaction_amt"].sum()
    category = category["transaction_amt"].sum()
    print(cat, round(off / category, 2), round(on / category, 2))
