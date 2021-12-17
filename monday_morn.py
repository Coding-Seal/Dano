import pandas
import pandas as pd
import plotly.graph_objects as go

data = pandas.read_csv("final.csv", sep=";")

data = data[data["day_time"] == 'Понедельник Вечер'][["code", "transaction_amt"]]
data = data.groupby(by=["code"]).sum()

data = data.reset_index()
data = data.sort_values("transaction_amt", ascending=True)
# print(data)

data = data[:10]
# print(data[["code", "transaction_amt"]])
y = data["code"]
q = []
for a in y:
    q.append( " и ".join(a.split(", ")[:2]))
y= pd.Series(q)


fig = go.Figure()

fig.add_bar(y=y, x=data["transaction_amt"], orientation="h")
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  font_size=25)
fig.update_xaxes(tickfont=dict(size=13))

fig.show()
