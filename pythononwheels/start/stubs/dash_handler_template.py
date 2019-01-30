
from {{appname}}.handlers.powhandler import PowHandler
from {{appname}}.config import myapp
from {{appname}}.application import app
import simplejson as json
import tornado.web
from tornado import gen
from {{appname}}.pow_dash import dispatcher
# Please import your model here. (from yourapp.models.dbtype)

@app.add_route("/dash.*", dispatch={"get" :"dash"})
@app.add_route("/_dash.*", dispatch={"get" :"dash_ajax", "post": "dash_ajax"})
class Dash(PowHandler):
    #
    # Sample dash handler to embedd dash into PythonOnWheels
    #  
    def dash(self, **kwargs):
        """ 
            This is the place where dash is called.
            dispatcher returns the HMTL including title, css, scripts and config via => dash.Dash.index()
            (See: in pow_dash.py => myDash.index)
            You can then insert the returned HTML into your template.
            I do this below in the self.render/self.success call => see base_dash.bs4 template (mustache like syntax)
        """
        print("processing dash method")
        #external_stylesheets = see config.py dash section
        retval = dispatcher(self.request, username="fake", session_id=1234, index=True)
        
        # 
        # this is the render template call which embeds the dash code (dash_block=retval)
        # from dispatcher (see above)
        self.render("dash_index.tmpl", dash_block=retval)
        # self.success(template="index.tmpl", dash_block=retval, data=res )

    
    def dash_ajax(self):
        """ 
            respond to the dash ajax / react request's 
        """
             
        print(" processing dash_ajax method")
       
        #
        # now hand over to the dispatcher
        #
        retval = dispatcher(self.request, index=False, username="fake", session_id=1234, powapp=self.application)
        
        self.set_header('Content-Type', 'application/json')
        self.write(retval)