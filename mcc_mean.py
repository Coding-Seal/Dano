import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go
from scipy import stats
from baskets import kras

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


def data_time(category_data,):
    """Expected data about one category"""

    category_data = quantile_outliers(category_data[["code", "transaction_amt",
                                                     "online_transaction_flg", "day_time"]], "transaction_amt")
    category_data = category_data.groupby("day_time").mean().reset_index()

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
    smth = {}
    for item, value in day.items():
        smth[shorts[item]] = value
    day = smth

    key = [i for i in range(1, 29)]
    key_day = day.keys()
    key = pd.Series(key).values.reshape(len(key), 1)
    key_day = pd.Series(key_day)
    for mcc in data.code.unique():
        print(mcc)

        data_mcc = data_time(data[data["code"] == mcc])
        if data_mcc is 0:
            continue
        data_mcc["day_time"] = data_mcc["day_time"].replace(shorts)

        x_data_mcc = data_mcc["day_time"].replace(day).values.reshape(len(data_mcc["day_time"]), 1)
        y_data_mcc = data_mcc["transaction_amt"].values

        if np.size(x_data_mcc):
            model_data_mcc = LinearRegression().fit(x_data_mcc, y_data_mcc)

        fig = go.Figure()
        # offline graph

        if np.size(x_data_mcc):
            fig.add_trace(go.Scatter(x=key_day, y=model_data_mcc.predict(key), name="trend",
                                     mode='lines+markers',
                                     marker=dict(color='Red')))
            fig.add_trace(go.Scatter(x=data_mcc["day_time"], y=data_mcc["transaction_amt"], mode='markers', name='',
                                     marker=dict(color='Red', size=10,
                                                 line=dict(color='MediumPurple', width=3))))
        # online graph

        mcc = " и ".join(mcc.split(", ")[:2])
        mcc = mcc.split("—")[0]
        fig.update_layout(legend_orientation="h",
                          paper_bgcolor='#fff',
                          plot_bgcolor='#fff',
                          font_size=17,
                          title=dict(text=mcc.split("(")[0],
                                     xanchor="center",
                                     x=0.5,
                                     y=0.99),
                          # y_error=dict(),
                          legend=dict(x=.5, xanchor="center", y=-0.5),
                          hovermode="x",
                          margin=dict(l=0, r=0, t=25, b=0))
        fig.update_traces(hoverinfo="all", hovertemplate="Аргумент: %{x}<br>Функция: %{y}")
        fig.update_yaxes(title="Средняя транзакция")
        print(mcc)
        fig.write_image(f"mcc_means/{mcc.replace('/', '|')}.png")
        # fig.write_image(f"{mcc.replace('/', '|')}.png")
        # fig.show()

        # break


print(1)
create_plot(data)
