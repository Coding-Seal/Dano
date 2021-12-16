import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go
from scipy import stats


def kras(n):
    day = dict([('Понедельник Утро', 1), ('Понедельник День', 8), ('Понедельник Вечер', 15), ('Понедельник Ночь', 22),
                ('Вторник Утро', 2), ('Вторник День', 9), ('Вторник Вечер', 16), ('Вторник Ночь', 23),
                ('Среда Утро', 3), ('Среда День', 10), ('Среда Вечер', 17), ('Среда Ночь', 24),
                ('Четверг Утро', 4), ('Четверг День', 11), ('Четверг Вечер', 18), ('Четверг Ночь', 25),
                ('Пятница Утро', 5), ('Пятница День', 12), ('Пятница Вечер', 19), ('Пятница Ночь', 26),
                ('Суббота Утро', 6), ('Суббота День', 13), ('Суббота Вечер', 20), ('Суббота Ночь', 27),
                ('Воскресенье Утро', 7), ('Воскресенье День', 14), ('Воскресенье Вечер', 21),
                ('Воскресенье Ночь', 28)])
    return n.replace(day)


data = pd.read_csv("final.csv", sep=";")
shorts = {'Воскресенье Вечер': "Вс В", 'Воскресенье День': "Вс Д", 'Воскресенье Ночь': "Вс Н",
          'Воскресенье Утро': "Вс У", 'Вторник Вечер': "Вт В", 'Вторник День': "Вт Д", 'Вторник Ночь': "Вт Н",
          'Вторник Утро': "Вт У", 'Понедельник Вечер': "Пн В", 'Понедельник День': "Пн Д", 'Понедельник Ночь': "Пн Н",
          'Понедельник Утро': "Пн У", 'Пятница Вечер': "Пт В", 'Пятница День': "Пт Д", 'Пятница Ночь': "Пт Н",
          'Пятница Утро': "Пт У", 'Среда Вечер': "Ср В", 'Среда День': "Ср Д", 'Среда Ночь': "Ср Н",
          'Среда Утро': "Ср У",
          'Суббота Вечер': "Сб В", 'Суббота День': "Сб Д", 'Суббота Ночь': "Сб Н", 'Суббота Утро': "Сб У",
          'Четверг Вечер': "Чт В", 'Четверг День': "Чт Д", 'Четверг Ночь': "Чт Н", 'Четверг Утро': "Чт У"}


def quantile_outliers(dataframe, column: str):
    """Deletes outliers form dataframe {sample} using Tukey's fences. Returns dataframe"""
    q25 = dataframe[column].quantile(0.25)
    q75 = dataframe[column].quantile(0.75)
    more = dataframe[column] >= q25 - 1.5 * (q75 - q25)
    less = dataframe[column] <= q75 + 1.5 * (q75 - q25)
    return dataframe[more & less]


def data_time(category_data, category, normalize=True):
    """Expected data about one category"""

    category_data = category_data[["code", "transaction_amt",
                                   "online_transaction_flg", "day_time"]]
    online = category_data[category_data["online_transaction_flg"] == "online"]
    offline = category_data[category_data["online_transaction_flg"] == "offline"]

    if normalize:
        # # online = online[(np.abs(stats.zscore(online["transaction_amt"])) < 3)]
        # # offline = offline[(np.abs(stats.zscore(offline["transaction_amt"])) < 3)]
        online = quantile_outliers(online, "transaction_amt")
        offline = quantile_outliers(offline, "transaction_amt")
    if online.code.count() + offline.code.count() < 100:
        return 0
    online = online.groupby("day_time").sum().reset_index()
    offline = offline.groupby("day_time").sum().reset_index()

    online["online_transaction_flg"] = np.ones(len(online))
    offline["online_transaction_flg"] = np.zeros(len(offline))

    category_data = pd.concat([online, offline])
    category_data.sort_values("day_time", key=kras)
    return category_data


def create_plot(data):
    day = dict([('Понедельник Утро', 1), ('Понедельник День', 8), ('Понедельник Вечер', 15), ('Понедельник Ночь', 22),
                ('Вторник Утро', 2), ('Вторник День', 9), ('Вторник Вечер', 16), ('Вторник Ночь', 23),
                ('Среда Утро', 3), ('Среда День', 10), ('Среда Вечер', 17), ('Среда Ночь', 24),
                ('Четверг Утро', 4), ('Четверг День', 11), ('Четверг Вечер', 18), ('Четверг Ночь', 25),
                ('Пятница Утро', 5), ('Пятница День', 12), ('Пятница Вечер', 19), ('Пятница Ночь', 26),
                ('Суббота Утро', 6), ('Суббота День', 13), ('Суббота Вечер', 20), ('Суббота Ночь', 27),
                ('Воскресенье Утро', 7), ('Воскресенье День', 14), ('Воскресенье Вечер', 21),
                ('Воскресенье Ночь', 28)])
    smth = {}
    for item, value in day.items():
        smth[shorts[item]] = value
    day = smth

    key = [i for i in range(1, 29)]
    key_day = day.keys()
    key = pd.Series(key).values.reshape(len(key), 1)
    key_day = pd.Series(key_day)

    for mcc in data.code.unique():
        data_mcc = data_time(data[data["code"] == mcc], mcc, normalize=True)
        if data_mcc is 0:
            continue
        data_mcc["day_time"] = data_mcc["day_time"].replace(shorts)

        offline = data_mcc[data_mcc["online_transaction_flg"] == 0].sort_values(by="day_time", key=kras)
        online = data_mcc[data_mcc["online_transaction_flg"] == 1].sort_values(by="day_time", key=kras)
        online["day_time"] = online["day_time"].replace(shorts)
        offline["day_time"] = offline["day_time"].replace(shorts)

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
            fig.add_trace(go.Scatter(x=key_day, y=model_offline.predict(key), name="offline_trend",
                                     mode='lines+markers',
                                     marker=dict(color='Blue')))
            fig.add_trace(go.Scatter(x=offline["day_time"], y=offline["transaction_amt"], mode='markers', name='',
                                     marker=dict(color='Blue', size=10,
                                                 line=dict(color='MediumPurple', width=3))))
        # online graph
        if np.size(x_online):
            fig.add_trace(go.Scatter(x=key_day, y=model_online.predict(key), name="online_trend",
                                     mode='lines+markers',
                                     marker=dict(color='Red')))
            fig.add_trace(go.Scatter(x=online["day_time"], y=online["transaction_amt"], mode='markers', name='',
                                     marker=dict(color='Red', size=10, line=dict(color='MediumPurple', width=3))))

        fig.update_layout(legend_orientation="h",
                          paper_bgcolor='#fff',
                          plot_bgcolor='#fff',
                          font_size=17,
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
        # fig.write_image(f"mcc_graphs/{mcc.replace('/', '|')}.png")
        # fig.write_image(f"{mcc.replace('/', '|')}.png")
        fig.show()
        break


create_plot(data)
