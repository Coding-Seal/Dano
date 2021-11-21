import numpy as np
import plotly.express as px
import pandas as pd
import customers
import baskets
import cat_distr

data = pd.read_csv('tink.csv')


def main():
    # print(data["category"].values())
    # customers.spending_bars(data)
    baskets.mean_basket_graph(data)
    #cat_distr.histogramm(data)


if __name__ == "__main__":
    main()
