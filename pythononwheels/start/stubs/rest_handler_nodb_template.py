from {{appname}}.handlers.base import BaseHandler
from {{appname}}.config import myapp
from {{appname}}.application import app
import tornado.web


# sample data
data = [
    {"1" : "one", "name" : "name_1" },
    {"2" : "two", "name" : "name_2"},
    {"3" : "three", "name" : "name_3"},
    {"4" : "four", "name" : "name_4"},
    {"5" : "five", "name" : "name_5"},
    {"6" : "six", "name" : "name_6"},
    {"7" : "seven", "name" : "name_7"}
}]

@app.add_rest_routes("{{handler_name}}")
class {{handler_class_name}}(BaseHandler):

    
    # 
    # every pow handler automatically gets these RESTful routes
    # when you add the : app.add_rest_routes() decorator.
    #
    # 1  GET    /todo                           #=> list
    # 2  GET    /todo/<uuid:identifier>         #=> show
    # 3  GET    /todo/new                       #=> new
    # 4  GET    /todo/<uuid:identifier>/edit    #=> edit 
    # 5  GET    /todo/page/<uuid:identifier>    #=> page
    # 6  GET    /todo/search                    #=> search
    # 7  PUT    /todo/<uuid:identifier>         #=> update
    # 8  PUT    /todo                           #=> update (You have to send the id as json payload)
    # 9  POST   /todo                           #=> create
    # 10 DELETE /todo/<uuid:identifier>         #=> destroy
    #

    # standard supported http methods are:
    # SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    # you can overwrite any of those directly or leave the @add_rest_routes out to have a basic 
    # handler.

    # curl test:
    # windows: (the quotes need to be escape in cmd.exe)
    #   (You must generate a post model andf handler first... update the db...)
    #   POST:   curl -H "Content-Type: application/json" -X POST -d "{ \"title\" : \"first {{handler_name}}\" }" http://localhost:8080/{{handler_name}}
    #   GET:    curl -H "Content-Type: application/json" -X GET http://localhost:8080/{{handler_name}}
    #   PUT:    curl -H "Content-Type: application/json" -X PUT -d "{ \"id\" : \"1\", \"text\": \"lalala\" }" http://localhost:8080/{{handler_name}}
    #   DELETE: curl -H "Content-Type: application/json" -X DELETE -d "{ \"id\" : \"1\" }" http://localhost:8080/{{handler_name}}
    
    model=Model()

    def show(self, id=None):
        try:
            self.success(message="{{handler_name}} show", data=data[id])
        except Exception as e:
            self.error(message="{{handler_name}} show: " + str(e))

    def list(self):
        self.success(message="{{handler_name}}, index", data=data)         
    
    def page(self, page=0):
        page_size=myapp["page_size"]
        page = int(page or 0)
        try:
            start_idx = (page*(page_size-1))
            end_idx = (page*page_size)+(page_size)
            self.success(
                message="rest_nodb page: #" + str(page), data=data[start_idx:end_idx] )  
        except Exception as e:
            self.error( message="base.error: rest_nodb page: " + str(e), data=data)
        
    @tornado.web.authenticated
    def edit(self, id=None):
        self.success(message="{{handler_name}}, edit id: " + str(id))

    @tornado.web.authenticated
    def new(self):
        self.success("{{handler_name}}, new")

    @tornado.web.authenticated
    def create(self):
        self.success(message="{{handler_name}}, create")

    @tornado.web.authenticated
    def update(self, id=None):
        self.success("{{handler_name}}, update id: " + str(id))

    @tornado.web.authenticated
    def destroy(self, id=None):
        self.success("{{handler_name}}, destroy id: " + str(id))
    
    def search(self):
        return self.error(message="{{handler_name}} search: not implemented yet" )
