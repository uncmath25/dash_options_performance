from dash import Dash, html
from flask import Flask

app = Flask(__name__)

EXTERNAL_STYLESHEETS = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'
]
dash_app = Dash(__name__, server=app, external_stylesheets=EXTERNAL_STYLESHEETS)
dash_app.css.config.server_locally = True

dash_app.layout = [html.Div(children='Dash Options Performance')]

if __name__ == '__main__':
    dash_app.run_server(host='0.0.0.0', port=5000, debug=True)
