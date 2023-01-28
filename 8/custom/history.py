import requests
import json
from plotly.utils import PlotlyJSONEncoder
import plotly.express as px
import pandas as pd

def createPlotHist(port):
    if port:
        if history := requests.get(f"http://127.0.0.1:{port}/history", timeout=10):
            tmp = json.loads(history.content.decode())
        else:
            tmp = {}
    else:
        tmp = {}

    count = {'date': [], 'count': []}
    for key, value in tmp.items():
        count['date'].append(key)
        count['count'].append(len(value))

    df = pd.DataFrame(count)
    fig = px.histogram(df, x="date", y="count")
    return json.dumps(fig, cls=PlotlyJSONEncoder)

def createPlotLine(port):
    if port:
        if history := requests.get(f"http://127.0.0.1:{port}/history", timeout=10):
            tmp = json.loads(history.content.decode())
        else:
            tmp = {}
    else:
        tmp = {}

    print(tmp)
    count = {'date': [], 'temperature': []}
    for key, value in tmp.items():
        count['date'].append(key)
        count['temperature'].append(value[0])

    df = pd.DataFrame(count)
    fig = px.line(df, x="date", y="temperature")
    return json.dumps(fig, cls=PlotlyJSONEncoder)