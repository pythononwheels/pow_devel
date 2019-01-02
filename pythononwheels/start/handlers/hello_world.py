import tornado.ioloop
import tornado.web
from testapp.handlers.base import BaseHandler
from testapp.application import app, route

@app.make_routes()
class HelloHandler(BaseHandler):
    @route(r'/hello', dispatch=["get"])
    def hello(self):
        self.write("Hello world!")