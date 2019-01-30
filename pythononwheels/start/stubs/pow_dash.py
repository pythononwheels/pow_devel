# -*- coding: utf-8 -*-
import sys
from random import randint

import dash
import dash_core_components as dcc
import dash_html_components as html
from {{appname}}.dash_components import Col, Row
from {{appname}}.config import myapp
from {{appname}}.config import mydash
import pandas as pd 
import datetime
from dash.dependencies import Input, Output 
import dash_dangerously_set_inner_html
from collections import OrderedDict
import plotly.graph_objs as go
import random
import requests
from tornado import httpclient

#
# Setup the embedded Dash App and create the actual dash layout, callbacks, etc.:
# see: _create_app()
# 

class myDash(dash.Dash):
    def index(self, *args, **kwargs):  # pylint: disable=unused-argument
        scripts = self._generate_scripts_html()
        css = self._generate_css_dist_html()
        config = self._generate_config_html()
        title = getattr(self, 'title', 'dashtest')
        
        return '''
            {}
            {}
            {}
        '''.format(css, config, scripts)
        
        # ret={
        #     "title" :   title,
        #     "css"   :   css,
        #     "config"    : config,
        #     "scripts"   : scripts
        # }


def _create_app_layout(*args, **kwargs):
    ''' 
        Creates the actual dash application and layout
        Just put any Dash layout in here.
        Documentation and examples: https://dash.plot.ly/

        The default route is: /dash which calls the handler/dash.py which creates the app
        and renders the pow_dash template.    
    '''
    df = pd.read_csv(
        'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

    #app = myDash(csrf_protect=False)
    #app.config['suppress_callback_exceptions']=True
    #
    # The Dash Layout
    # This is rendered in views/pow_dash.tmpl -> { raw dash_block }
    # When you 
    app.layout = html.Div([
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()}
        )
    ])


    @app.callback(
        dash.dependencies.Output('graph-with-slider', 'figure'),
        [dash.dependencies.Input('year-slider', 'value')])
    def update_figure(selected_year):
        filtered_df = df[df.year == selected_year]
        traces = []
        for i in filtered_df.continent.unique():
            df_by_continent = filtered_df[filtered_df['continent'] == i]
            traces.append(go.Scatter(
                x=df_by_continent['gdpPercap'],
                y=df_by_continent['lifeExp'],
                text=df_by_continent['country'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ))

        return {
            'data': traces,
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    return app.layout

# create the app once
app = myDash(csrf_protect=False)
app.config['suppress_callback_exceptions']=True
#app.layout=_create_app_layout()
#app.layout=html.Div([
#            dcc.Graph()
#])

def dispatcher(request, index=True, **kwargs):
    '''
        Dispatch the Dash and Dash Ajax requests
    '''
    kwargs["external_stylesheets"] = mydash["external_stylesheets"]
    #
    # only serve the base layout once. 
    # 
    if index:
        app.layout = _create_app_layout(**kwargs)
    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.headers.get('Content-type')
    }
    with app.server.test_request_context(request.path, **params):
        app.server.preprocess_request()
        try:
            response = app.server.full_dispatch_request()
        except Exception as e:
            response = app.server.make_response(app.server.handle_exception(e))
            print(70*"=")
            print("done dash dispatching")
            print(70*"=")
        return response.get_data()
    
