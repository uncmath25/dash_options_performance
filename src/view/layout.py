import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


INPUT_OPTION_NAME_ID = 'OPTION_NAME'
INPUT_START_STOCK_PRICE_ID = 'START_STOCK_PRICE'
INPUT_OPTION_PRICE_ID = 'OPTION_PRICE'
INPUT_STRIKE_PRICE_ID = 'STRIKE_PRICE'
INPUT_OPTION_NUMBER_ID = 'OPTION_NUMBER'
INPUT_POTENTIAL_STOCK_PRICE_MULTIPLIER_ID = 'POTENTIAL_STOCK_PRICE_MULTIPLIER'
OUTPUT_BREAK_EVEN_PROFIT_PRICE_ID = 'BREAK_EVEN_PROFIT_PRICE'
OUTPUT_MULTIPLIER_ID = 'MULTIPLIER'
OUTPUT_FIGURE_ID = 'FIGURE'

OPTION_NAME_DEFAULT = 'IBIT_CALL_Jan_16_26_75'
START_STOCK_PRICE_DEFAULT = 56.76
OPTION_PRICE_DEFAULT = 15.01
STRIKE_PRICE_DEFAULT = 75
OPTION_NUMBER_DEFAULT = 20
POTENTIAL_STOCK_PRICE_MULTIPLIER_DEFAULT = 5

SPACING_DIV = html.Div(style=dict(padding='10px'))


def build_layout():
    return dbc.Container([
        dbc.Container([
            _build_spacing_div(5),
            dbc.Row([
                dbc.Col(
                    html.H1('Options Performance Calculator')
                )
            ]),
            _build_spacing_div(5),
            dbc.Row([
                dbc.Col([
                    html.H5('Option Name:'),
                    dcc.Input(OPTION_NAME_DEFAULT, type='text', id=INPUT_OPTION_NAME_ID, style={'width': '100%'})
                ], width=2),
                dbc.Col([
                    html.H5('Stock Start Price:'),
                    dcc.Input(START_STOCK_PRICE_DEFAULT, type='number', id=INPUT_START_STOCK_PRICE_ID)
                ], width=2),
                dbc.Col([
                    html.H5('Option Price:'),
                    dcc.Input(OPTION_PRICE_DEFAULT, type='number', id=INPUT_OPTION_PRICE_ID)
                ], width=2),
                dbc.Col([
                    html.H5('Strike Price:'),
                    dcc.Input(STRIKE_PRICE_DEFAULT, type='number', id=INPUT_STRIKE_PRICE_ID)
                ], width=2),
                dbc.Col([
                    html.H5('Option Number:'),
                    dcc.Input(OPTION_NUMBER_DEFAULT, type='number', id=INPUT_OPTION_NUMBER_ID)
                ], width=2),
                dbc.Col([
                    html.H5('Stock Price Multiplier:'),
                    dcc.Input(POTENTIAL_STOCK_PRICE_MULTIPLIER_DEFAULT, type='number',
                              id=INPUT_POTENTIAL_STOCK_PRICE_MULTIPLIER_ID)
                ], width=2)
            ]),
            _build_spacing_div(5),
            dbc.Row([
                dbc.Col([
                    html.H5('Break Even Profit Price:'),
                ], width=3),
                dbc.Col([
                    html.H5(id=OUTPUT_BREAK_EVEN_PROFIT_PRICE_ID)
                ], width=3),
                dbc.Col([
                    html.H5('Multiplier:'),
                ], width=3),
                dbc.Col([
                    html.H5(id=OUTPUT_MULTIPLIER_ID)
                ], width=3)
            ]),
            _build_spacing_div(5),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id=OUTPUT_FIGURE_ID, style={'height': '70vh'})
                )
            ])
        ])
    ], fluid=True)


def _build_spacing_div(pixels):
    return html.Div(style=dict(padding=f'{pixels}px'))
