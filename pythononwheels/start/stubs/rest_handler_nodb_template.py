from {{appname}}.handlers.powhandler import PowHandler
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
class {{handler_class_name}}(PowHandler):
    """ 
    every pow handler automatically gets these RESTful routes
    when you add the : app.add_rest_routes() decorator.
    
    1  GET    /{{handler_name}}                           #=> list
    2  GET    /{{handler_name}}/<uuid:identifier>         #=> show
    3  GET    /{{handler_name}}/new                       #=> new
    4  GET    /{{handler_name}}/<uuid:identifier>/edit    #=> edit 
    5  GET    /{{handler_name}}/page/<uuid:identifier>    #=> page
    6  GET    /{{handler_name}}/search                    #=> search
    7  PUT    /{{handler_name}}/<uuid:identifier>         #=> update
    8  PUT    /{{handler_name}}                           #=> update (You have to send the id as json payload)
    9  POST   /{{handler_name}}                           #=> create
    10 DELETE /{{handler_name}}/<uuid:identifier>         #=> destroy
    
    Standard supported http methods are:
    SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    you can overwrite any of those directly or leave the @add_rest_routes out to have a basic 
    handler.

    curl tests:
     for windows: (the quotes need to be escape in cmd.exe)
      (You must generate a post model andf handler first... update the db...)
      POST:   curl -H "Content-Type: application/json" -X POST -d "{ \"title\" : \"first {{handler_name}}\" }" http://localhost:8080/{{handler_name}}
      GET:    curl -H "Content-Type: application/json" -X GET http://localhost:8080/{{handler_name}}
      PUT:    curl -H "Content-Type: application/json" -X PUT -d "{ \"id\" : \"1\", \"text\": \"lalala\" }" http://localhost:8080/{{handler_name}}
      DELETE: curl -H "Content-Type: application/json" -X DELETE -d "{ \"id\" : \"1\" }" http://localhost:8080/{{handler_name}}
    """
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
