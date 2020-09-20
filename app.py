import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


app.layout = html.Div([
    html.Label('Choose min support'),
    dcc.RangeSlider(
        min=0.101,
        max=0.709,
        step=0.03,
        value=[0.101,0.709],
        marks={i for i in range(0.101,0.709)}
    )
   
    
])

if __name__ == '__main__':
    app.run_server(debug=True)
