import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc, State, no_update
from QFClasses.markowitz_model import MarkoModel

def layout():
    available_stocks = ["AAPL", "WMT", "TSLA", "GE", "AMZN", "DB"]
    
    return dbc.Container([
        html.H1('Markowitz Model'),
        html.P("""
               The Modern Portfolio Theory (MPT) was intoduced by Harry Markowitz in 1952 with the aim of finding an optimal investent portfolio.
               While a very simplistic approach, it is one that been widely used since and is still a foundation of investment theory.
               MPT creates the most efficient portfolio through diversification. By including multiple, uncorrelated stocks in a portfolio to minimize specific risk while maximising return.
               
               The base example here combines 6 stocks and will build out a stock chooser.
               """),
        
        # Dropdown for stock selection and DatePickers for date range
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='stock-dropdown',
                    options=[{'label': stock, 'value': stock} for stock in available_stocks],
                    multi=True,
                    value=["AAPL", "WMT", "TSLA", "GE", "AMZN", "DB"],  # default values
                    placeholder="Select stocks"
                ),
                width=4
            ),
            dbc.Col(
                dcc.DatePickerSingle(
                    id='start-date-picker',
                    date='2012-01-01',
                    display_format='YYYY-MM-DD',
                    placeholder="Start Date"
                ),
                width=4
            ),
            dbc.Col(
                dcc.DatePickerSingle(
                    id='end-date-picker',
                    date='2017-01-01',
                    display_format='YYYY-MM-DD',
                    placeholder="End Date"
                ),
                width=4
            )
        ], className='mb-3'),

        # Button to generate graph
        dbc.Row([
            dbc.Col(
                html.Button('Generate Graph', id='generate-graph', n_clicks=0),
                width={"size": 2, "offset": 5}  # Center the button
            )
        ], className='mb-3'),

        # Graph
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='marko-graph', figure={}),
                className='mb-3'
            )
        ]),
        # optimal details
        dbc.Row([
        dbc.Col([
            html.H5("Stock Weightings"),
            html.Div(id='stock-weightings-table')
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.H5("Portfolio Details"),
            html.Div(id='details-table')
        ])
    ])
    ])

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
        details_table = dbc.Table.from_dataframe(details_df, striped=True, bordered=True, hover=True)

        return graph_figure, stock_weightings_table, details_table