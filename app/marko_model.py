import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc, State, no_update
from QFClasses.markowitz_model import MarkoModel
from components import CARD_STYLE

def layout():
    available_stocks = ["AAPL", "WMT", "TSLA", "GE", "AMZN", "DB"]

    # Create a Card for the introduction and instructions
    intro_card = dbc.Card(
        dbc.CardBody([
            html.H1('Markowitz Model'),
            html.P("""
                   The Modern Portfolio Theory (MPT) was introduced by Harry Markowitz in 1952 with the aim of finding an optimal investment portfolio.
                   While a very simplistic approach, it is one that has been widely used since and is still a foundation of investment theory.
                   MPT creates the most efficient portfolio through diversification. By including multiple, uncorrelated stocks in a portfolio to minimize specific risk while maximizing return.

                   The base example here combines 6 stocks and will build out a stock chooser.
                   """),
        ]),
        className="mb-3",
        style=CARD_STYLE
    )

    # Grouping dropdown and date pickers
    selection_card = dbc.Card(
        dbc.CardBody([
            dbc.Row([
                
                dbc.Col([
                    html.P("Choose which stocks you would like to include in your portfolio."),
                    dcc.Dropdown(
                        id='stock-dropdown',
                        options=[{'label': stock, 'value': stock} for stock in available_stocks],
                        multi=True,
                        value=["AAPL", "WMT", "TSLA", "GE", "AMZN", "DB"],  # default values
                        placeholder="Select stocks"
                    )],
                    width=6
                ),
                dbc.Col(html.P(), width=2),
                dbc.Col(
                    [html.P("Buy date:"),
                        dcc.DatePickerSingle(
                        id='start-date-picker',
                        date='2012-01-01',
                        display_format='YYYY-MM-DD',
                        placeholder="Start Date"
                    )],
                    width=2
                ),
                dbc.Col(
                    [html.P("Sell date:"),
                        dcc.DatePickerSingle(
                        id='end-date-picker',
                        date='2017-01-01',
                        display_format='YYYY-MM-DD',
                        placeholder="End Date"
                    )],
                    width=2
                )
            ], className='mb-3')
        ]),
        className="mb-3",
        style=CARD_STYLE
    )
    
    
    output_graphs = dbc.Card(
        dbc.CardBody([
            dbc.Row(
                [dbc.Col([
                html.H5("Stock Weightings"),
                html.Div(id='stock-weightings-table'),
            ]),
                dbc.Col([
                html.H5("Portfolio Details"),
                html.Div(id='details-table')
            ]) 
            ], className='mb-3')
        ]),
        style=CARD_STYLE
    )

    return dbc.Container(
        [
            intro_card,
            selection_card,
            dbc.Button('Generate Graph', id='generate-graph', color="primary", className="w-20"),
            
            # Wrapping the components with dcc.Loading
            dcc.Loading(
                id="loading",
                type="cube",  # can be "default", "circle", "dot", or "cube"
                children=[
                    dcc.Graph(id='marko-graph', figure={}, style={"width": "70%", "height": "400px", "margin": "auto"}),
                    output_graphs
                ]
            )
        ],
        fluid=True,
        style={"padding": "20px", "backgroundColor": "#CDEAD6"}  # Light background color
    )

def register_callbacks(app):
    @app.callback(
        [
        Output('marko-graph', 'figure'),
        Output('stock-weightings-table', 'children'),
        Output('details-table', 'children')
    ],
        [Input('generate-graph', 'n_clicks')],
        [Input('stock-dropdown', 'value')],
        [Input('start-date-picker', 'date')],
        [Input('end-date-picker', 'date')]
    )
    def update_marko_model(n_clicks, selected_stocks, start_date, end_date):
        if n_clicks == 0:
            return no_update, no_update

        marko = MarkoModel(stocks=selected_stocks, start_date=start_date, end_date=end_date)
        dataset = marko.download_data()
        log_daily_returns = marko.calculate_return(dataset)
        pweights, means, risks = marko.generate_portfolios(log_daily_returns)

        graph_figure = marko.show_optimal_portfolio(
            marko.optimise_portfolio(pweights, log_daily_returns),
            log_daily_returns,
            means,
            risks
        )

        optimal_details = marko.print_optimal_port(
            marko.optimise_portfolio(pweights, log_daily_returns),
            log_daily_returns
        )

        stock_weightings, details_df = marko.print_optimal_port(
            marko.optimise_portfolio(pweights, log_daily_returns),
            log_daily_returns
        )

        stock_weightings_table = dbc.Table.from_dataframe(stock_weightings, striped=True, bordered=True, hover=True)
        details_table = dbc.Table.from_dataframe(details_df, striped=True, bordered=True, hover=True, style={"color": "#D9F6CC"})

        return graph_figure, stock_weightings_table, details_table