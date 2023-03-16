
import tornado.web
import tornado.escape
import json
import werkzeug.security 
import os
from {{appname}}.config import myapp 
from {{appname}}.handlers.base import BaseHandler
from {{appname}}.handlers.powhandlermixin import PowHandlerMixin
from tornado.websocket import WebSocketHandler

class PowWsHandler(PowHandlerMixin, WebSocketHandler):
    """
        The Base Pow Websocket Handler 
        This is Place to put common stuff for all your 
        WebSocket handlers which will remain unaffected by any PoW Changes.
        Purely and only User or Extension controlled.
    """
   