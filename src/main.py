from dash import Dash
from dash.dependencies import Input, Output
from flask import Flask

from controller.callback import build_fig, compute_break_even_profit_price, compute_multiplier
import view.layout as layout


app = Flask(__name__)

EXTERNAL_STYLESHEETS = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'
]
dash_app = Dash(__name__, server=app, external_stylesheets=EXTERNAL_STYLESHEETS)
dash_app.css.config.server_locally = True

dash_app.layout = layout.build_layout()
dash_app.callback(
    Output(layout.OUTPUT_BREAK_EVEN_PROFIT_PRICE_ID, 'children'),
    Input(layout.INPUT_START_STOCK_PRICE_ID, 'value'),
    Input(layout.INPUT_OPTION_PRICE_ID, 'value'),
    Input(layout.INPUT_STRIKE_PRICE_ID, 'value'),
    Input(layout.INPUT_OPTION_NUMBER_ID, 'value')
)(compute_break_even_profit_price)
dash_app.callback(
    Output(layout.OUTPUT_MULTIPLIER_ID, 'children'),
    Input(layout.INPUT_START_STOCK_PRICE_ID, 'value'),
    Input(layout.INPUT_OPTION_PRICE_ID, 'value'),
    Input(layout.INPUT_STRIKE_PRICE_ID, 'value'),
    Input(layout.INPUT_OPTION_NUMBER_ID, 'value'),
    Input(layout.INPUT_POTENTIAL_STOCK_PRICE_MULTIPLIER_ID, 'value')
)(compute_multiplier)
dash_app.callback(
    Output(layout.OUTPUT_FIGURE_ID, 'figure'),
    Input(layout.INPUT_OPTION_NAME_ID, 'value'),
    Input(layout.INPUT_START_STOCK_PRICE_ID, 'value'),
    Input(layout.INPUT_OPTION_PRICE_ID, 'value'),
    Input(layout.INPUT_STRIKE_PRICE_ID, 'value'),
    Input(layout.INPUT_OPTION_NUMBER_ID, 'value'),
    Input(layout.INPUT_POTENTIAL_STOCK_PRICE_MULTIPLIER_ID, 'value')
)(build_fig)

if __name__ == '__main__':
    dash_app.run_server(host='0.0.0.0', port=5000, debug=True)
