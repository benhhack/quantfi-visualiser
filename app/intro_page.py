import dash_bootstrap_components as dbc
from dash import html
from components import CARD_STYLE 

def intro_layout():
    # Introduction Card
    intro_me = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col(
                [
                    html.H2('Hello, my name is', style={"margin-bottom": "10px", "fontWeight":"bold", "color": "#269682"}),
                    html.H1("Benjamin Hack", style={"margin-bottom": "20px", "fontWeight":"bold", "color": "#11453B"}),
                    html.P("""
                           I am a software developer and data enthusiast, passionate about exploring the underlying structure of the world's random financial markets. """, className="lead"),
                ], width=8),
            dbc.Col(
                html.Img(src="/assets/mephoto.jpg", style={"width": "180px", "border-radius": "20%", "margin-top": "10px"}),
                width=4, align="center"
            )
        ], align="center"),
        html.Hr(),  # Horizontal line for separation
        html.P([
            "Outside of work, I enjoy football, golf, chess, and music. I've also been diving down the cryptocurrency rabbit hole. Feel free to connect with me on ",
            html.A("LinkedIn", href="https://www.linkedin.com/in/benjaminhhack", target='_blank', style={"color":"#828FFF"}),
            " or check out my ",
            html.A("GitHub", href="https://www.github.com/benhhack", target='_blank', style={"color":"#828FFF"}),
        ], style={"margin-top": "20px"})
    ]),
    className="mb-3",
    style=CARD_STYLE
)

    # Project Introduction Card
    project_intro = dbc.Card(
        dbc.CardBody([
            html.H1('About The Project'),
            html.P("""This project leverages the Markowitz Model, a cornerstone of Modern Portfolio Theory (MPT). Introduced by Harry Markowitz in 1952, the model aims to find the optimal investment portfolio by diversifying to maximize returns while minimizing specific risks.""", className="lead"),
            html.P("""Here, I present a tool to visualize the optimal portfolio given a set of stocks and a specified time frame. Using both historical data and sophisticated algorithms, this tool provides insights into how assets can be weighted within a portfolio to achieve the desired balance of risk and return."""),
            html.Br(),
            html.P("""The design and implementation of this tool are results of comprehensive research, rigorous coding, and continuous testing. Your feedback and suggestions are always appreciated.""")
        ]),
        className="mb-3",
        style=CARD_STYLE
    )

    return dbc.Container(
        [
            intro_me,
            project_intro
        ],
        fluid=True,
        style={"padding": "20px", "backgroundColor": "#E9F5E8"}  # Slightly different shade for a refreshing feel
    )