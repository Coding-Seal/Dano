import pandas as pd
import plotly.express as px
from random import shuffle, randint

data = pd.read_csv("tink.csv")


def pie_time():
    smt = data.groupby("time_of_day").sum().reset_index()
    fig = px.pie(smt, "time_of_day", "transaction_amt", title="Сумма транзакций",
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 )
    fig.update_traces(textfont_size=35,
                      sort=False
                      )

    fig.update_layout(
        legend_font_size=45,
        title_font_size=50,
        title_xanchor="right",
        title_x=0.62,
        title_pad_b=25,

    )

    fig.show()


def pie_day():
    smt = data.groupby("day_of_week").count().reset_index()
    fig = px.pie(smt, "day_of_week", "transaction_amt", title="Сумма транзакций",
                 color_discrete_sequence=px.colors.qualitative.Dark2,
                 )
    fig.update_traces(textfont_size=35,
                      sort=False
                      )

    fig.update_layout(
        legend_font_size=45,
        title_font_size=50,
        title_xanchor="right",
        title_x=0.62,
        title_pad_b=25,

    )
    fig.show()


def histogram():
    smt = data.groupby("time_of_day").sum().reset_index()

    fig = px.histogram(smt.sort_values("transaction_amt"), "time_of_day", "transaction_amt",)
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Сумма транзакций")
    # fig.update_traces(textfont_size=35,
    #                   )
    #

    fig.update_layout(
        plot_bgcolor="#fff",
        font_size=30

    )
    fig.show()
histogram()