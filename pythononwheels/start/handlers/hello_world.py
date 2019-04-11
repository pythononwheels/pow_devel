import tornado.ioloop
import tornado.web
from {{appname}}.handlers.base import BaseHandler
from {{appname}}.application import app, route

@app.make_routes()
class HelloHandler(BaseHandler):
    @route(r'/hello', dispatch=["get"])
    def hello(self):
        self.write("Hello world!")