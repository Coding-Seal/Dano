import numpy as np
import plotly.express as px
import pandas as pd

def histogramm(data):
    fig = px.histogram(data, "category")
    fig.show()
    return None