import pandas as pd
import plotly.express as px
from random import shuffle, randint

xui = ['rgb(255, 255, 224)', 'rgb(255, 228, 225)', 'rgb(119, 136, 153)',
       'rgb(238, 130, 238)', 'rgb(60, 179, 113)', 'rgb(127, 255, 212)', 'rgb(255, 182, 193)']
for i in range(randint(0, 10)):
    shuffle(xui)
data = pd.read_csv("final.csv", sep=";")
data = data[data["category"] == "Супермаркеты"][["code", "transaction_amt"]]
data = data.groupby("code").sum().reset_index()

fig = px.pie(data, "code", "transaction_amt", color="code", color_discrete_sequence=xui)
fig.update_layout(legend_font_size=20)

fig.show()
