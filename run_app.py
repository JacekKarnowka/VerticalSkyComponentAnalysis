import app_main
from flask import Flask, send_from_directory, send_file
import dash
import dash_bootstrap_components as dbc

server = Flask(__name__)

app = dash.Dash(
    "VSC-analysis", external_stylesheets=[dbc.themes.BOOTSTRAP], server=server
)

if __name__ == "__main__":
    app.run_server(debug=False)