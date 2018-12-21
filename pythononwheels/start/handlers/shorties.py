import tornado.ioloop
import tornado.web
from {{appname}}.handlers.base import BaseHandler
from {{appname}}.application import app

# You can uese flask/werkzeug routing.
# @app.add_route('/test/<uuid:identifier>', dispatch={"get" : "testuuid"})
# Or you can use regex in the routes as well:
# (r"/([^/]+)/(.+)", ObjectHandler),
# any regex goes. any group () will be handed to the handler 
# see example handler below.



@app.add_route("/", pos=1)
@app.add_route('/index/<int:year>', dispatch={"get" : "test"})
#@app.add_route('/index/<uuid:identifier>', dispatch={"get" : "testuuid"})
#@app.add_route('/index/<uuid:identifier>.<format>', dispatch={"get" : "testuuid"})
class IndexdHandler(BaseHandler):
    def get(self, year=None):
        print(" Calling IndexHandler from handlers/shorties.py: parameter index: " + str(year))
        self.render("index.tmpl")
    
    def get(self, year=None):
        print(" Calling IndexHandler from handlers/shorties.py: parameter index: " + str(year))
        self.render("index.tmpl")
    
    def testuuid(self, identifier=None, format=None):
        print(" Calling Indexhandler. Indentifier: {}, format: {}".format(str(identifier), str(format)))
        self.render("index.tmpl")

# this will be the last route since it has the lowest pos.
@app.add_route(".*", pos=0)
class ErrorHandler(BaseHandler):
    def get(self):
        return self.error( template="404.tmpl", http_code=404  )


