import requests
import json
import plotly
import plotly.express as px
import pandas as pd

def createPlot(port):
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
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)