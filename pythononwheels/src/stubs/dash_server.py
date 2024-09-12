
from flask import Flask
from dash import Dash
from {{appname}}.conf.config import mydash

# should start and end with a '/'
URL_BASE_PATHNAME = '/'

server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
    url_base_pathname=URL_BASE_PATHNAME,
    external_stylesheets=mydash["external_stylesheets"],
    external_scripts=mydash["external_scripts"]
    #suppress_callback_exceptions = True
)

app.config['suppress_callback_exceptions'] = True