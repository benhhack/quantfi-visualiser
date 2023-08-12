import os
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import components
from callbacks import get_callbacks

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True


app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])

server = app.server

content = html.Div(id="page-content", style=components.CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), components.sidebar, content])


get_callbacks(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug)
