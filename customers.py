import numpy as np
import plotly.express as px
import pandas as pd

def extract_customers_data(data):

    customers = {}
    basket = []
    for customer in data.customer_id.unique():
        basket.append(np.sum(data[data["customer_id"] == customer]["transaction_amt"]))

    customers["customer_id"] = [str(i) for i in data.customer_id.unique()]
    customers["money_spent"] = basket

    return pd.DataFrame(customers)


def spending_bars(data):
    """The whole dataframe expected"""
    customers = extract_customers_data(data)
    customers = customers.sort_values(by="money_spent", ascending=False)

    fig = px.bar(customers, x="customer_id", y="money_spent")
    fig.show()
    return None
