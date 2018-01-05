import tornado.ioloop
import tornado.web
from {{appname}}.handlers.base import BaseHandler
from {{appname}}.application import app

# you can use regex in the routes as well:
# (r"/([^/]+)/(.+)", ObjectHandler),
# any regex goes. any group () will be handed to the handler 
# 

# if you specify a method, this method will be called for this route
@app.add_route("/thanks/*", dispatch={"get": "_get"} )
@app.add_route("/thanks/([0-9]+)*", dispatch={"get": "testme"})
class ThanksHandler(BaseHandler):
    def _get(self):
        print("  .. in _get" )
        self.render("thanks.tmpl")

    def testme(self, index=0 ):
        print("  .. in testme: index = " + str(index))
        self.render("thanks.tmpl", index=index)
    
# if you DON't specify a method, the standard HTTP verb method (e.g. get(), put() will be called)
@app.add_route("/index/([0-9]+)*")
@app.add_route("/", pos=1)
class IndexdHandler(BaseHandler):
    def get(self, index=None):
        print(" Calling IndexHandler from handlers/shorties.py: parameter index: " + str(index))
        self.render("index.tmpl")

# this will be the last route since it has the lowest pos.
@app.add_route(".*", pos=0)
class ErrorHandler(BaseHandler):
    def get(self):
        return self.error( template="404.tmpl", http_code=404  )

@app.add_route("/test/([0-9]+)*", dispatch={"get" : "test"})
class TestHandler(BaseHandler):
    # on HTTP GET this method will be called. See dispatch parameter.
    def test(self, index=None):
        self.write(index)
    
@app.add_rest_routes("rest")
class RestHandler(BaseHandler):
    # on HTTP GET this method will be called. See config.py "default_rest_route"
    def list(self):
        self.write("REST")


@app.add_route('/werkzeug/<int:year>', dispatch={"get" : "test"})
@app.add_route('/werkzeug/<uuid:identifier>', dispatch={"get" : "testuuid"})
@app.add_route('/werkzeug/<uuid:identifier>.<format>', dispatch={"get" : "testuuid"})
class WerkzeugTestHandler(BaseHandler):
    # on HTTP GET this method will be called. See dispatch parameter.
    def test(self, year=None):
        self.write("I got year: " + str(year))
    
    def testuuid(self, anotherone=None, identifier=None, format="html"):
        self.write("I got uuid: " + str(identifier)
                    + "<hr> I got anotherone ? == " + str(anotherone)
        )

@app.add_route("/errortest", dispatch={"get" : "errortest"})
class ErrorTestHandler(BaseHandler):
    # on HTTP GET this method will be called. See dispatch parameter.
    def errortest(self):
        self.error(message="ERRORTEST", data=[])