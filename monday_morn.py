import pandas
import plotly.graph_objects as go

data = pandas.read_csv("final.csv", sep=";")

data = data[data["day_time"] == 'Понедельник Вечер'][["code", "transaction_amt"]]
data = data.groupby(by=["code"]).sum()

data = data.reset_index()
data = data.sort_values("transaction_amt", ascending=False)
print(data)

data = data[:10]
# print(data[["code", "transaction_amt"]])

fig = go.Figure()

fig.add_bar(x=data["code"], y=data["transaction_amt"])
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)', )
fig.update_xaxes(tickfont=dict(size=13))

fig.show()
