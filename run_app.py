from flask import Flask
import dash
import dash_bootstrap_components as dbc

# Import files
import app_main

# Run Flask server
# Create dash app, based on external stylesheets and Flask server

server = Flask(__name__)

app = dash.Dash(
    "VSC-analysis", external_stylesheets=[dbc.themes.BOOTSTRAP], server=server
)

if __name__ == "__main__":
    app_main.app.run_server(debug=True)
