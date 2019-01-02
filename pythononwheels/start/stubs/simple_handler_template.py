#from {{appname}}.handlers.base import BaseHandler
from {{appname}}.handlers.powhandler import PowHandler
from {{appname}}.config import myapp
from {{appname}}.models.{{model_type}}.{{handler_name}} import {{handler_model_class_name}} as Model
from {{appname}}.config import myapp, database
from {{appname}}.application import app
import simplejson as json
import tornado.web
from tornado import gen
# Please import your model here. (from yourapp.models.dbtype)

@app.add_route('/{{handler_name}}/test/<int:testval>', dispatch={"get" : "_get_method"})
class {{handler_class_name}}(PowHandler):
    
    # your DB model
    model=Model()
    #
    # on HTTP GET this method will be called. See dispatch parameter.
    #
    def _get_method(self, testval=0):
        """
            just a simple hanlder sceleton. Adapt to your needs
        """ 
        m=Model()
        out_dict = {
            "testval"   : str(testval),
            "model"     : m.to_json()
        }
        self.success(message="I got testval:", data=out_dict, format="json", raw_data=True)
        #self.write("I got testval:" + str(testval))
    
