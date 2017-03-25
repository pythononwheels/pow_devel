from {{appname}}.handlers.base import BaseHandler
from {{appname}}.config import myapp
from {{appname}}.application import app
import tornado.web


# sample data
data = {
    "1" : "one",
    "2" : "two",
    "3" : "three",
    "4" : "four",
    "5" : "five",
    "6" : "six",
    "7" : "seven"
}

@app.add_rest_routes("{{handler_name}}")
class {{handler_name}}Handler(BaseHandler):

    # 
    # every pow handler automatically gets these RESTful routes
    # thru the @app.add_rest_routes() decorator.
    #
    # 1  GET    /{{handler_name}}        #=> list
    # 2  GET    /{{handler_name}}/1      #=> show
    # 3  GET    /{{handler_name}}/new    #=> new
    # 4  GET    /{{handler_name}}/1/edit #=> edit 
    # 5  GET    /{{handler_name}}/page/1 #=> page
    # 6  GET    /{{handler_name}}/search #=> search
    # 7  PUT    /{{handler_name}}/1      #=> update
    # 8  POST   /{{handler_name}}        #=> create
    # 9  DELETE /{{handler_name}}/1      #=> destroy
    #

    # standard supported http methods are:
    # SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    # you can overwrite any of those directly or leave the @add_rest_routes out to have a basic 
    # handler.
    
    # sample data
    data = {
        "1" : "one",
        "2" : "two",
        "3" : "three",
        "4" : "four",
        "5" : "five",
        "6" : "six",
        "7" : "seven",
    }

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
                 
    def search(self):
        return self.error(message="{{handler_name}} search: " + not implemented yet )
        
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
