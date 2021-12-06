import numpy as np
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from baskets import kras
from scipy import stats


def rid_of_outliers(dirty_data):
    time = pd.Series(['Понедельник Утро', 'Понедельник День', 'Понедельник Вечер', 'Понедельник Ночь', 'Вторник Утро',
                      'Вторник День', 'Вторник Вечер', 'Вторник Ночь', 'Среда Утро', 'Среда День', 'Среда Вечер',
                      'Среда Ночь',
                      'Четверг Утро', 'Четверг День', 'Четверг Вечер', 'Четверг Ночь', 'Пятница Утро', 'Пятница День',
                      'Пятница Вечер', 'Пятница Ночь', 'Суббота Утро', 'Суббота День', 'Суббота Вечер', 'Суббота Ночь',
                      'Воскресенье Утро', 'Воскресенье День', 'Воскресенье Вечер', 'Воскресенье Ночь'])

    dirty_data = dirty_data.sort_values("transaction_amt")
    outliers = int(len(dirty_data) * 0.04)
    dirty_data = dirty_data[outliers: len(dirty_data) - outliers]
    df = pd.DataFrame()


def data_time(data,category , normalize=True):
    """Expected data about one category"""

    category_data = data[["category", "transaction_amt",
                          "online_transaction_flg", "day_time"]]
    online = category_data[category_data["online_transaction_flg"] == "online"]
    offline = category_data[category_data["online_transaction_flg"] == "offline"]
    if normalize:
        online = online[(np.abs(stats.zscore(data["transaction_amt"])) < 3)]
        offline = offline[(np.abs(stats.zscore(data["transaction_amt"])) < 3)]

    online = online.groupby("day_time").sum().reset_index()
    offline = offline.groupby("day_time").sum().reset_index()

    online["online_transaction_flg"] = np.ones(len(online))
    offline["online_transaction_flg"] = np.zeros(len(offline))
    category_data = pd.concat([online, offline])
    category_data.sort_values("day_time", key=kras)
    return category_data


def graph(data):
    categories = data_time(data)
    # fig = px.line(supermarket, x="day_time", y="transaction_amt", color="online_transaction_flg")
    # fig.show()
    fig = make_subplots(rows=34, cols=2)
    for i, category in enumerate(categories):
        offline = category[category["online_transaction_flg"] == 0]
        online = category[category["online_transaction_flg"] == 1]

        fig.append_trace(
            go.Scatter(x=offline["day_time"], y=offline["transaction_amt"]), row=i,
            col=1)
