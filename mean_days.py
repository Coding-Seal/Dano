import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go

data = pd.read_csv("final.csv", sep=";")
shorts = {'Воскресенье Вечер': "Вс В", 'Воскресенье День': "Вс Д", 'Воскресенье Ночь': "Вс Н",
          'Воскресенье Утро': "Вс У", 'Вторник Вечер': "Вт В", 'Вторник День': "Вт Д", 'Вторник Ночь': "Вт Н",
          'Вторник Утро': "Вт У", 'Понедельник Вечер': "Пн В", 'Понедельник День': "Пн Д", 'Понедельник Ночь': "Пн Н",
          'Понедельник Утро': "Пн У", 'Пятница Вечер': "Пт В", 'Пятница День': "Пт Д", 'Пятница Ночь': "Пт Н",
          'Пятница Утро': "Пт У", 'Среда Вечер': "Ср В", 'Среда День': "Ср Д", 'Среда Ночь': "Ср Н",
          'Среда Утро': "Ср У",
          'Суббота Вечер': "Сб В", 'Суббота День': "Сб Д", 'Суббота Ночь': "Сб Н", 'Суббота Утро': "Сб У",
          'Четверг Вечер': "Чт В", 'Четверг День': "Чт Д", 'Четверг Ночь': "Чт Н", 'Четверг Утро': "Чт У"}


def kras(smth):
    a = {'Пн У': 1, 'Вт У': 2, 'Ср У': 3, 'Чт У': 4, 'Пт У': 5, 'Сб У': 6, 'Вс У': 7, 'Пн Д': 8, 'Вт Д': 9, 'Ср Д': 10,
         'Чт Д': 11, 'Пт Д': 12, 'Сб Д': 13, 'Вс Д': 14, 'Пн В': 15, 'Вт В': 16, 'Ср В': 17, 'Чт В': 18, 'Пт В': 19,
         'Сб В': 20, 'Вс В': 21, 'Пн Н': 22, 'Вт Н': 23, 'Ср Н': 24, 'Чт Н': 25, 'Пт Н': 26, 'Сб Н': 27, 'Вс Н': 28}

    smth = smth.replace(a)
    return smth


def quantile_outliers(dataframe, column: str):
    """Deletes outliers form dataframe {sample} using Tukey's fences. Returns dataframe"""
    q25 = dataframe[column].quantile(0.25)
    q75 = dataframe[column].quantile(0.75)
    more = dataframe[column] >= q25 - 1.5 * (q75 - q25)
    less = dataframe[column] <= q75 + 1.5 * (q75 - q25)
    return dataframe[more & less]


def data_time(category_data, ):
    """Expected data about one category"""

    category_data = quantile_outliers(category_data[["code", "transaction_amt",
                                                     "online_transaction_flg", "day_time"]], "transaction_amt")
    category_data = category_data.groupby("day_time").mean().reset_index()

    category_data.sort_values("day_time", key=kras)
    return category_data


def create_plot(data):
    a = {'Пн У': 1, 'Вт У': 2, 'Ср У': 3, 'Чт У': 4, 'Пт У': 5, 'Сб У': 6, 'Вс У': 7, 'Пн Д': 8, 'Вт Д': 9, 'Ср Д': 10,
         'Чт Д': 11, 'Пт Д': 12, 'Сб Д': 13, 'Вс Д': 14, 'Пн В': 15, 'Вт В': 16, 'Ср В': 17, 'Чт В': 18, 'Пт В': 19,
         'Сб В': 20, 'Вс В': 21, 'Пн Н': 22, 'Вт Н': 23, 'Ср Н': 24, 'Чт Н': 25, 'Пт Н': 26, 'Сб Н': 27, 'Вс Н': 28}

    key = [i for i in range(1, 29)]
    key_day = a.keys()
    key = pd.Series(key).values.reshape(len(key), 1)
    key_day = pd.Series(key_day)
    for mcc in data.code.unique():

        data_mcc = data_time(data[data["code"] == mcc])
        if data_mcc is 0:
            continue
        data_mcc["day_time"] = data_mcc["day_time"].replace(shorts)
        data_mcc = data_mcc.sort_values("day_time", key=kras)
        # print(data_mcc.day_time)

        x_data_mcc = kras(data_mcc["day_time"]).values.reshape(len(data_mcc["day_time"]), 1)
        # print(x_data_mcc)
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
        fig.write_image(f"mcc_days/{mcc.replace('/', '|')}.png")
        # fig.write_image(f"{mcc.replace('/', '|')}.png")
        # fig.show()

        # break


print(1)
create_plot(data)
