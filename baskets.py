import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


def mean_category_data(data):
    category = data[["category", "transaction_amt"]].groupby("category").sum() / len(data.customer_id.unique())
    return category.reset_index()


def mean_basket_graph(data):
    category = mean_category_data(data)
    fig = px.pie(category, "category", "transaction_amt")
    fig.show()


def kras(smth):
    day = {'Воскресенье Вечер': 27, 'Воскресенье День': 26, 'Воскресенье Ночь': 28,
           'Воскресенье Утро': 25, 'Вторник Вечер': 7, 'Вторник День': 6, 'Вторник Ночь': 8,
           'Вторник Утро': 5, 'Понедельник Вечер': 3, 'Понедельник День': 2, 'Понедельник Ночь': 4,
           'Понедельник Утро': 1, 'Пятница Вечер': 19, 'Пятница День': 18, 'Пятница Ночь': 20,
           'Пятница Утро': 17, 'Среда Вечер': 11, 'Среда День': 10, 'Среда Ночь': 12, 'Среда Утро': 9,
           'Суббота Вечер': 23, 'Суббота День': 22, 'Суббота Ночь': 24, 'Суббота Утро': 21,
           'Четверг Вечер': 15, 'Четверг День': 14, 'Четверг Ночь': 16, 'Четверг Утро': 13}
    smth = smth.replace(day)
    return smth


def category_graph(data, category):
    # fig = make_subplots(rows=1, cols=2,specs=[{"type": "scatter"}, {"type": "scatter"}])
    # fig.add_trace(px.scatter(data, x="day_time", y= "amt_transaction"))
    categories = data[data["category"] == category]
    fig = px.scatter(categories, x="day_time", y="transaction_amt")
    fig.show()
