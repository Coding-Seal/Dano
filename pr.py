import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from exper import data_time
import plotly.graph_objs as go
from scipy import stats

data = pd.read_csv("modified.csv")

day = dict([('Понедельник Утро', 1), ('Понедельник День', 2), ('Понедельник Вечер', 3), ('Понедельник Ночь', 4),
            ('Вторник Утро', 5), ('Вторник День', 6), ('Вторник Вечер', 7), ('Вторник Ночь', 8),
            ('Среда Утро', 9), ('Среда День', 10), ('Среда Вечер', 11), ('Среда Ночь', 12),
            ('Четверг Утро', 13), ('Четверг День', 14), ('Четверг Вечер', 15), ('Четверг Ночь', 16),
            ('Пятница Утро', 17), ('Пятница День', 18), ('Пятница Вечер', 19), ('Пятница Ночь', 20),
            ('Суббота Утро', 21), ('Суббота День', 22), ('Суббота Вечер', 23), ('Суббота Ночь', 24),
            ('Воскресенье Утро', 25), ('Воскресенье День', 26), ('Воскресенье Вечер', 27), ('Воскресенье Ночь', 28)])

data["day_time"] = data["day_time"].replace(day)
category = "Супермаркеты"
data = data_time(data[data["category"] == category], category, normalize=True)
data = data[data["online_transaction_flg"] == 0]

x = data["day_time"].values.reshape(len(data["day_time"]), 1)

y = data["transaction_amt"].values

model = LinearRegression().fit(x, y)

fig = go.Figure()
fig.add_trace(go.Scatter(x=data["day_time"].values, y=model.predict(x), name="regression", mode='lines+markers', ))
fig.add_trace(go.Scatter(x=data["day_time"], y=y, mode='markers', name='',
                         marker=dict(color='LightSkyBlue', size=20, line=dict(color='MediumPurple', width=3))))
fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, xanchor="center"),
                  hovermode="x",
                  margin=dict(l=0, r=0, t=0, b=0))
fig.update_traces(hoverinfo="all", hovertemplate="Аргумент: %{x}<br>Функция: %{y}")
fig.show()
