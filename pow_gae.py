import string
import os.path
import sys
import os
from pprint import pformat
#from beaker.middleware import SessionMiddleware
from cgi import parse_qs, escape
import traceback, StringIO
import webob
#
# google app-engine imports

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app



def powapp(environ, start_response):
    
    basepath = "./"
    #basepath = environ.get("pow.wsgi_dir")
    sys.path.append(os.path.normpath(basepath + "/lib"))
    sys.path.append(os.path.normpath(basepath + "/controllers"))
    sys.path.append(os.path.normpath(basepath + "/models"))
    import powlib
    
    output = []
    powdict =  {}    
    real_action = None
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/html')
        ]
    
    #TODO: add GAE session management     
    #powdict["SESSION"] = session
    
    
    
    powdict["PARAMETERS"] = plist
    
    powdict["SCRIPT_VIEWS_DIR"] = os.path.abspath(os.path.join(os.path.dirname(environ.get("SCRIPT_FILENAME")) + "/views/"))
    powdict["STYLESHEET_LINK_TAG"] = os.path.abspath(os.path.join(os.path.dirname(environ.get("SCRIPT_FILENAME")) + "/views/stylesheets/"))
    # PATH_INFO contains the path beginning from the app-root url.     # first part is the controller,      # second part is the action
    powdict["PATH_INFO"] = environ.get("PATH_INFO")
    powdict["POW_APP_NAME"] = environ.get("pow.app_name")
    powdict["POW_APP_DIR"] = environ.get("pow.wsgi_dir")
    powdict["FLASHTEXT"] = ""
    
        
    #
    # get controller and action
    #
    pathdict = get_controller_and_action(environ["PATH_INFO"])
    controller = powdict["CONTROLLER"] = pathdict["controller"]
    action = powdict["ACTION"] = pathdict["action"]
    powdict["PATHDICT"]=pathdict
    controller = string.capitalize(controller) + "Controller"
   
    
    #
    # route the request
    #   
    aclass = powlib.load_class(controller,controller)
    aclass.setCurrentAction(action)
    if hasattr( aclass, action ):
        real_action = eval("aclass." + action)
        
    output.append(real_action(powdict).encode('utf-8'))
    
    start_response(status, response_headers)
    return output
        


#application= SessionMiddleware(powapp, key='mysession', secret='randomsecret')
#application = SessionMiddleware(powapp, session_opts)
application = powapp

    
def show_environ( environ ):
    ostr = ""
    ostr +=  "<h1>Sorted Keys an Values in <tt>environ</tt></h1>" 
    
    sorted_keys = environ.keys()
    sorted_keys.sort()
    
    for key in sorted_keys:
        ostr += str(key) + " = " + str(environ.get(key)) + "<br>"
        
    return ostr
        
def get_http_get_parameters( environ):
    #
    # parameters are in query sting
    #
    plist = []
    pstr = ""
    pstr = environ.get("QUERY_STRING")
    if pstr != "":
        plist = pstr.split("&")        
    odict = {}
    for elem in plist:
        key,val = string.split(elem,"=")
        odict[key]= val
    return odict

def get_http_post_parameters( environ ):
    instr = None
    plist = None
    odict = {}
    instr= environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    plist = string.split(instr,"&")
    for elem in plist:
        key,val = string.split(elem,"=")
        newval = val.replace("+", " ")
        odict[key] = newval
    return odict

def is_post_request( environ ):
    if environ['REQUEST_METHOD'].upper() != 'POST':
        return False
    else:
        return True

def is_get_request( environ ):
    if environ['REQUEST_METHOD'].upper() != 'GET':
        return False
    else:
        return True
    
def get_controller_and_action(pi):
    # converts a path_info: /user/list/1/2/3/4
    # into al list ol = ['4', '3', '2', '1', 'list', 'user']
    # where the controller is always the last element and the action the one before that (len(ol)-1) and len(ol)-2)
    ol = []
    l = []
    l= os.path.split(pi)
    ol.append(l[1])
    while l[0] != "/":
        #print "l[0]:" + l[0]
        #print "l[1]:" + l[1]
        l = os.path.split(l[0])
        ol.append(l[1])
        print ol
    
    pl = []
    nicedict = {}
    nicedict["controller"]=ol[len(ol)-1]
    nicedict["action"]=ol[len(ol)-2]
    for c in range(0,len(ol)-2):
        pl.append(ol[c])
    nicedict["parameters"]=pl
    
    return nicedict

    
def main():
#   run_wsgi_app(webapp_add_wsgi_middleware(application))
    run_wsgi_app(application)

if __name__ == "__main__":
    main()