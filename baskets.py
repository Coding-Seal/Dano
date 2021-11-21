import numpy as np
import plotly.express as px
import pandas as pd


def extarct_category_data(data):
    category = data[["category", "transaction_amt"]].groupby("category").sum() / len(data.customer_id.unique())
    result = {"category": data["category"].unique(),
              'spent': category["transaction_amt"]}
    return pd.DataFrame(result)


def mean_basket_graph(data):
    category = extarct_category_data(data)
    fig = px.pie(category, "category", "spent")
    fig.show()

