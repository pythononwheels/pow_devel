#from {{appname}}.handlers.base import BaseHandler
from {{appname}}.handlers.powhandler import PowHandler
from {{appname}}.models.{{model_type}}.{{handler_name}} import {{handler_model_class_name}} as Model
from {{appname}}.config import myapp, database
from {{appname}}.application import app
import tornado.web

@app.add_rest_routes("{{handler_name}}")
class {{handler_class_name}}(PowHandler):

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
    
    def show(self, id=None):
        m=Model()
        res=m.find_one({{handler_model_class_name}}.id==id)
        self.success(message="{{handler_model_class_name}} show", data=res.json_dump())

    def list(self):
        m=Model()
        res = m.find_all(as_json=True)
        self.success(message="{{handler_model_class_name}}, index", data=res)         
    
    def page(self, page=0):
        m=Model()
        page_size=myapp["page_size"]
        if database["type"] == "sqlite":
            limit=page_size
        else:
            limit=(page*page_size)+page_size
        res = m.find_all(as_json=True, 
            limit=limit,
            offset=page*page_size
            )
        self.success(message="{{handler_model_class_name}} page: #" +str(page), data=res )  
    
    def search(self):
        return self.error(message="{{handler_name}} search: not implemented yet ")
        
    @tornado.web.authenticated
    def edit(self, id=None):
        self.success(message="{{handler_model_class_name}}, edit id: " + str(id))

    @tornado.web.authenticated
    def new(self):
        self.success("{{handler_model_class_name}}, new")

    @tornado.web.authenticated
    def create(self):
        self.success(message="{{handler_model_class_name}}, create")

    @tornado.web.authenticated
    def update(self, id=None):
        self.success("{{handler_model_class_name}}, update id: " + str(id))

    @tornado.web.authenticated
    def destroy(self, id=None):
        self.success("{{handler_model_class_name}}, destroy id: " + str(id))
