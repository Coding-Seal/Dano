import numpy as np
import plotly.express as px
import pandas as pd
import customers

data = pd.read_csv('tink.csv')


def main():
    customers.spending_bars(data)


if __name__ == "__main__":
    main()
