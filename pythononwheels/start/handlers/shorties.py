import tornado.ioloop
import tornado.web
from {{appname}}.handlers.base import BaseHandler
from {{appname}}.application import app, route

# ROUTING:
# You can decorate routes on the handler classes or on the methods directly.
# 
# You can use flask/werkzeug style routing.
#      example: @app.add_route('/test/<uuid:identifier>', dispatch={"get" : "testuuid"})
# Or you can use regex in the routes as well:
#      example: @route('/test/([0-9]+)', dispatch=["get"] )
#      any regex goes. any group () will be handed to the handler 
#      see example handler below.
# 
# Check the docs for more info: https://www.pythononwheels.org/documentation
#

@app.add_route(r"/", dispatch={"get" : "index"}, pos=1)
@app.make_routes()
class IndexdHandler(BaseHandler):
    def index(self, year=None):
        """
            Example Method with class attached routing (see above "/" )
        """
        print(" Calling IndexHandler.index from handlers/shorties.py: parameter index: " + str(year))
        self.render("index.tmpl")
    
    @route(r'/test/<int:identifier>', dispatch=["get"])
    def testuuid(self, identifier=None, format=None):
        """
            Example method with Method attached route and Flask style route
        """
        print(" Calling Indexhandler.tetuuid Indentifier: {}, format: {}".format(str(identifier), str(format)))
        self.render("index.tmpl")
    
    @route(r"/story/([0-9]+)", dispatch=["get"])
    def get_story(self, identifier=None, format=None):
        """
            Example method with Method attached route and tornado/regex style route
        """
        print(" Calling Indexhandler.get_story Indentifier: {}, format: {}".format(str(identifier), str(format)))
        self.render("index.tmpl")

@app.add_route(r"/testresults", dispatch={"get" : "show_results"})
class PyTestHandler(BaseHandler):
    def show_results(self):
        """
            this action will show the pytest from test/runtests.py 
        """
        self.render("result.html")
    
# this will be the last route since it has the lowest pos.
@app.add_route(r".*", pos=0)
class ErrorHandler(BaseHandler):
    def get(self):
        return self.error( template="404.tmpl", http_code=404  )


