# WSGI main script to be executed by WSGI capable
# Webservers. 
# www.pythononwheels.org runs with this script 
# Served by Apache and mod_wsgi. (on Debian Linux)
#
# 
import string
import os.path
import sys
import os
import re
from pprint import pformat
from beaker.middleware import SessionMiddleware
#from cgi import parse_qs, escape
import cgi

import traceback, StringIO
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./config" )))
#sys.path.append(os.path.normpath("/var/www/pow/lib"))
#sys.path.append(os.path.normpath("/var/www/pow/config"))

import powlib
import pow_web_lib
import urllib
import pow
import powlib
import pow_web_lib
from webob import Request, Response

# one of: 
#    NORMAL  = print >> environ['wsgi.errors'], almost nothing
#    INFO    = more Info print >> environ['wsgi.errors'],ed (But especially NOT the whole WSGI environment)
#    DEBUG   = All Info print >> environ['wsgi.errors'],ed, including WSGI environment. (LONG)
MODE_NORMAL = 1
MODE_INFO = 2
MODE_DEBUG = 3

MODE = MODE_NORMAL


def powapp_simple_server(environ, start_response):
    
    #print >> environ['wsgi.errors'], show_environ_cli(environ)
    output = []
    powdict =  {}    
    real_action = None
    
    req = Request(environ)
    req.charset = pow.global_conf["DEFAULT_ENCODING"]
    
    
    #print >> environ['wsgi.errors'], dir(req.params)
    #
    #alias_dict ={}
    environ["SCRIPT_FILENAME"] = __file__
    powdict["POW_APP_NAME"] = "PythonOnWheels"
    powdict["POW_APP_URL"] = "www.pythononwheels.org"
    powdict["POW_APP_DIR"] = environ.get("pow.wsgi_dir")
    powdict["ERROR_INFO"] = ""
    
    # Get the session object from the environ
    session = environ['beaker.session']
    #TO_DO: set the right status in the end, according to the situatio instead of setting it hard-coded here
    status = '200 OK'
    response_headers = [
        #('Content-type', 'text/html; charset=utf-8')
        ('Content-type', 'text/html')
        ]

    
    if not session.has_key('user.id'):
        session['user.id'] = 0
    
    #session.save()
    
    powdict["SESSION"] = session
    print >> environ['wsgi.errors'], "-- session:", session.keys()
    print >> environ['wsgi.errors'], "-- PoW: req.content_type: ", req.content_type
    print >> environ['wsgi.errors'], "-- PoW: req.method", req.method
    print >> environ['wsgi.errors'], "-- PoW: path_info", environ["PATH_INFO"]
    print >> environ['wsgi.errors'], "-- PoW: req.params", req.params
    print >> environ['wsgi.errors'], "-- PoW: req.body", req.body
    #print >> environ['wsgi.errors'], "-- PoW: ", req.environ
    print >> environ['wsgi.errors'], "-- PoW: req.path_url", req.path_url
    print >> environ['wsgi.errors'], "-- PoW: req.application_url: ", req.application_url

    
    powdict["REQ_CONTENT_TYPE"] = req.content_type
    powdict["REQ_PARAMETERS"] = req.params
    powdict["REQ_BODY"] = req.body
    
    print >> environ['wsgi.errors'], powdict["REQ_PARAMETERS"]
    
    if MODE > MODE_NORMAL: 
        print >> environ['wsgi.errors'], plist
        print >> environ['wsgi.errors'], plist.keys()
    plist = req.params
    
    #if plist.has_key("image"):
    #    print >> environ['wsgi.errors'], "Image found: " +  plist['image'].filename
    #    ofile = file(plist['image'].filename, "wb")
    #    infile = plist['image'].file
    #    ofile.write( infile.read() )
    #   #ofile.write( plist["image"].value )
    #    ofile.close()
    #
    # handling static files
    #
    pinfo = environ.get("PATH_INFO")
    pinfo_before = pinfo
    ostr = ""
    #
    # check for static links and replace them when found.
    #
    found_static = False
    #for elem in alias_dict:
    #    if string.find(pinfo,  elem) != -1:
    #        found_static = True
    #        pinfo = string.replace(pinfo,elem, alias_dict[elem])
    
    print >> environ["wsgi.errors"], pinfo
    environ["PATH_INFO"] = pinfo
    #
    # in the pow_router.wsgi (mod_wsgi) environment static files
    # are completely handled by the webserver (e.g. apache) so the script
    # does not need to care about that.
    #
    #if found_static == True:
    #    print >> environ['wsgi.errors'], "-- Static REQUEST --------------------------------------------------------- "
    #    non_binary = [".css", ".html",".js",".tmpl"]
    #    ctype = "UNINITIALIZED"
    #    ftype = os.path.splitext(pinfo)[1]
    #    
    #    if string.lower(ftype) in non_binary:
    #        infile = open (os.path.normpath(pinfo), "r")
    #    else:
    #        infile = open (os.path.normpath(pinfo), "rb")
    #    ostr = infile.read()
    #    infile.close()
    #    #print >> environ['wsgi.errors'], "file type is: ", ftype, " -> ", ctype
    #    if string.lower(ftype) == ".gif":
    #        ctype = "image/gif"
    #    elif string.lower(ftype) == ".jpg" or string.lower(ftype) ==".jpeg":
    #        ctype= "image/jpeg"
    #    elif string.lower(ftype) == ".css":
    #        ctype = "text/css"
    #    elif string.lower(ftype) == ".png":
    #        ctype = "image/png"
    #    elif string.lower(ftype) ==".js":
    #        ctype= "application/x-javascript"
    #    else:
    #        ctype = "text/html"
    #    #print >> environ['wsgi.errors'], "file type is: ", ftype, " responding with type-> ", ctype
    #    response_headers = [
    #        ('Content-type', ctype )
    #    ]
    #    start_response(status, response_headers)
    #    return [ostr]
        
    print >> environ['wsgi.errors'], "-- Dynamic REQUEST --------------------------------------------------------- "
    if MODE > MODE_INFO :
        print >> environ['wsgi.errors'], "Request: " + environ["REQUEST_METHOD"] + " " + environ["PATH_INFO"] + " " + environ["SERVER_PROTOCOL"] + " " + environ["QUERY_STRING"]    
        print >> environ['wsgi.errors'], "PATH_INFO before: ", pinfo_before
        print >> environ['wsgi.errors'], "PATH_INFO after: ", pinfo
    
    if not session.has_key('counter'):
        session['counter'] = 0
    else:
        session['counter'] += 1

    powdict["SCRIPT_FILENAME"] = environ.get("SCRIPT_FILENAME")
    powdict["SCRIPT_DIR"] = os.path.dirname(environ.get("SCRIPT_FILENAME"))
    powdict["SCRIPT_VIEWS_DIR"] = os.path.abspath(os.path.join(os.path.dirname(environ.get("SCRIPT_FILENAME")) + "/views/"))
    # PATH_INFO contains the path beginning from the app-root url.     # first part is the controller,      # second part is the action
    powdict["PATH_INFO"] = environ.get("PATH_INFO")
    #print >> environ['wsgi.errors'], os.path.split(powdict["PATH_INFO"])
    powdict["ENVIRON"] = pow_web_lib.show_environ( environ )
    powdict["DOCUMENT_ROOT"] = environ.get("DOCUMENT_ROOT")
    powdict["FLASHTEXT"] = ""
    powdict["FLASHTYPE"] ="error"
    #output.append( show_environ( output, environ ) )
    
    #
    # get controller and action
    #
    pathdict = {}
    if environ["PATH_INFO"] != "":
       pathdict = pow_web_lib.get_controller_and_action(environ["PATH_INFO"])
    else:
	pathdict["controller"]  = ""
        pathdict["action"]  = ""
    #(controller,action) = os.path.split(pathinfo)
    print >> environ['wsgi.errors'], "(controller,action) -> (" + pathdict["controller"] + "," + pathdict["action"] +")"
    controller = powdict["CONTROLLER"] = pathdict["controller"]
    action = powdict["ACTION"] = pathdict["action"]
    powdict["PATHDICT"]=pathdict

    #TO_DO: include the real, mod re based routing instead of seting it hard to user/list here.
    if controller == "":
        defroute = pow.routes["default"]
        #defroute = powlib.readconfig("pow.cfg","routes","default")
        print >> environ['wsgi.errors'], pow_web_lib.get_controller_and_action(defroute)
        pathdict = pow_web_lib.get_controller_and_action(defroute)
        #(controller,action) = os.path.split(pathinfo)
        print >> environ['wsgi.errors'], "(controller,action) -> ", pathdict
        controller = powdict["CONTROLLER"] = pathdict["controller"]
        action = powdict["ACTION"] = pathdict["action"]
        powdict["PATHDICT"]=pathdict

        print >> environ['wsgi.errors'], "Using the DEFAULT_ROUTE: ",
        print >> environ['wsgi.errors'], "(controller,action) -> ", pathdict
    # get rid of the first / in front of the controller. string[1:] returns the string from char1 to len(string)
    controller = string.capitalize(controller) + "Controller"
    
    #
    # route the request
    #
    print >> environ['wsgi.errors'], "Loading Class:", controller
    try:
        aclass = powlib.load_class(controller,controller)
        print >> environ['wsgi.errors'], "setting Action: ", action
        aclass.setCurrentAction(action)
        #output.append(action + "<br>")
        # checking if action is locked 
        if aclass.is_locked(action):
            # locked, so set the action to the given redirection and execute that instead.
            # TODO: Could be aditionally coupled with a flashtext.
            print >> environ['wsgi.errors'], "Action: ", action, " locked."
            aclass.setCurrentAction(aclass.get_redirection_if_locked(action))
            action = aclass.get_redirection_if_locked(action)
            print >> environ['wsgi.errors'], " -- Redirecting to: ", action
        #
        # Now really execute the action
        #
        if hasattr( aclass, action ):
            real_action = eval("aclass." + action)
            output.append(real_action(powdict).encode(pow.global_conf["DEFAULT_ENCODING"]))
        else:
            msg = "ERROR: No such class or action  %s.%s " % (controller, action)  
            output.append(msg)
    except Exception, e:
        # TODO: needs to be really redesigned AND really to rely on request routing.
        #   -> only enough for pre Beta 1
        # if neither controller , nor action where found. Fallback to app/welcome.
        aclass = powlib.load_class("App","App")
        print >> environ['wsgi.errors'], "setting Action: ", "welcome"
        aclass.setCurrentAction("welcome")
        #output.append(action + "<br>")
        if hasattr( aclass, action ):
            real_action = eval("aclass." + action)
            output.append(real_action(powdict).encode(pow.global_conf["DEFAULT_ENCODING"]))
        else:
            msg = "ERROR: No such class or action  %s.%s " % (controller, action)  
            output.append(msg)
    #
    # error handling wsgi see: http://www.python.org/dev/peps/pep-0333/#error-handling
    #
    start_response(status, response_headers)
    return output
        
session_opts = {
    'session.type': 'file',
    'session.data_dir': '/var/www/pow/session_data',
    'session.cookie_expires': True,
    'session.auto': True
}

#application= SessionMiddleware(powapp, key='mysession', secret='randomsecret')
#application = SessionMiddleware(powapp, session_opts)
#application = pow_web_lib.Middleware(SessionMiddleware(powapp_simple_server, session_opts))
application = SessionMiddleware(powapp_simple_server, session_opts)

