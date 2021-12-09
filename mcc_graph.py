import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go
from scipy import stats
from baskets import kras

data = pd.read_csv("final.csv", sep=";")


def data_time(category_data, category, normalize=True):
    """Expected data about one category"""

    category_data = category_data[["code", "transaction_amt",
                                   "online_transaction_flg", "day_time"]]
    online = category_data[category_data["online_transaction_flg"] == "online"]
    offline = category_data[category_data["online_transaction_flg"] == "offline"]
    if normalize:
        online = online[(np.abs(stats.zscore(online["transaction_amt"])) < 3)]
        offline = offline[(np.abs(stats.zscore(offline["transaction_amt"])) < 3)]

    online = online.groupby("day_time").sum().reset_index()
    offline = offline.groupby("day_time").sum().reset_index()

    online["online_transaction_flg"] = np.ones(len(online))
    offline["online_transaction_flg"] = np.zeros(len(offline))
    category_data = pd.concat([online, offline])
    category_data.sort_values("day_time", key=kras)
    return category_data


def create_plot(data):
    day = dict([('Понедельник Утро', 1), ('Понедельник День', 2), ('Понедельник Вечер', 3), ('Понедельник Ночь', 4),
                ('Вторник Утро', 5), ('Вторник День', 6), ('Вторник Вечер', 7), ('Вторник Ночь', 8),
                ('Среда Утро', 9), ('Среда День', 10), ('Среда Вечер', 11), ('Среда Ночь', 12),
                ('Четверг Утро', 13), ('Четверг День', 14), ('Четверг Вечер', 15), ('Четверг Ночь', 16),
                ('Пятница Утро', 17), ('Пятница День', 18), ('Пятница Вечер', 19), ('Пятница Ночь', 20),
                ('Суббота Утро', 21), ('Суббота День', 22), ('Суббота Вечер', 23), ('Суббота Ночь', 24),
                ('Воскресенье Утро', 25), ('Воскресенье День', 26), ('Воскресенье Вечер', 27),
                ('Воскресенье Ночь', 28)])
    key = [i for i in range(1, 29)]
    key_day = day.keys()
    key = pd.Series(key).values.reshape(len(key), 1)
    key_day = pd.Series(key_day)

    for mcc in data.code.unique():
        data_mcc = data_time(data[data["code"] == mcc], mcc, normalize=True)
        offline = data_mcc[data_mcc["online_transaction_flg"] == 0].sort_values(by="day_time", key=kras)
        online = data_mcc[data_mcc["online_transaction_flg"] == 1].sort_values(by="day_time", key=kras)
        x_offline = offline["day_time"].replace(day).values.reshape(len(offline["day_time"]), 1)
        y_offline = offline["transaction_amt"].values

        x_online = online["day_time"].replace(day).values.reshape(len(online["day_time"]), 1)
        y_online = online["transaction_amt"].values
        if np.size(x_offline):
            model_offline = LinearRegression().fit(x_offline, y_offline)
        if np.size(x_online):
            model_online = LinearRegression().fit(x_online, y_online)

        fig = go.Figure()
        # offline graph
        if np.size(x_offline):
            fig.add_trace(go.Scatter(x=key_day, y=model_offline.predict(key), name="offline_regression",
                                     mode='lines+markers',
                                     marker=dict(color='LightSkyBlue')))
            fig.add_trace(go.Scatter(x=offline["day_time"], y=offline["transaction_amt"], mode='markers', name='',
                                     marker=dict(color='LightSkyBlue', size=10,
                                                 line=dict(color='MediumPurple', width=3))))
        # online graph
        if np.size(x_online):
            fig.add_trace(go.Scatter(x=key_day, y=model_online.predict(key), name="online_regression",
                                     mode='lines+markers',
                                     marker=dict(color='Red')))
            fig.add_trace(go.Scatter(x=online["day_time"], y=online["transaction_amt"], mode='markers', name='',
                                     marker=dict(color='Red', size=10, line=dict(color='MediumPurple', width=3))))

        fig.update_layout(legend_orientation="h",
                          title=dict(text=" и ".join(mcc.split(", ")[:2]),
                                     xanchor="center",
                                     x=0.5,
                                     y=0.99),
                          # y_error=dict(),
                          legend=dict(x=.5, xanchor="center", y=-0.5),
                          hovermode="x",
                          margin=dict(l=0, r=0, t=25, b=0))
        fig.update_traces(hoverinfo="all", hovertemplate="Аргумент: %{x}<br>Функция: %{y}")
        print(mcc)
        fig.write_image(f"mcc_graphs/{mcc.replace('/', '|')}.png")
        # fig.write_image(f"{mcc.replace('/', '|')}.png")
        # break



create_plot(data)
