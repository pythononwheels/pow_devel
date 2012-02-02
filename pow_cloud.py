import string
import os.path
import sys
import os
from pprint import pformat
from beaker.middleware import SessionMiddleware
from cgi import parse_qs, escape
import traceback, StringIO
#
# you have to adapt the include path below manually. The pow_router script is executed in the os.getcwd() of
# the webserver. For xampp this might be (on windows) c:\xampp. so if your app is in 
# c:\xampp\cgi-bin\pow\aktuell\manuell your include path would be as shown below.
#
#sys.path.append(os.path.normpath("./cgi-bin/pow/aktuell/manuell/lib"))
#sys.path.append(os.path.normpath("./cgi-bin/pow/aktuell/manuell/controllers"))
#sys.path.append(os.path.normpath("./cgi-bin/pow/aktuell/manuell/models"))

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
	# Get the session object from the environ
	session = environ['beaker.session']

	if not session.has_key('counter'):
		session['counter'] = 0
	session['counter'] += 1
	if not session.has_key('user.id'):
		session['user.id'] = 0
	
	#session.save()
	
	#output.append("<hr>sess counter" + str(session["counter"])+"<hr>")
	#if session.has_key("user.id"):
	#	output.append("<hr>sess user.id" + str(session["user.id"])+"<hr>")
	#else:
	#	output.append("<hr>sess user.id = None<hr>")
	
	powdict["SESSION"] = session
	
	if is_get_request(environ):
		plist = get_http_get_parameters(environ)
	elif is_post_request(environ):
		plist = get_http_post_parameters(environ)
	else:
		return
	
	powdict["PARAMETERS"] = plist
	powdict["SCRIPT_FILENAME"] = environ.get("SCRIPT_FILENAME")
	powdict["SCRIPT_DIR"] = os.path.dirname(environ.get("SCRIPT_FILENAME"))
	powdict["SCRIPT_VIEWS_DIR"] = os.path.abspath(os.path.join(os.path.dirname(environ.get("SCRIPT_FILENAME")) + "/views/"))
	powdict["STYLESHEET_LINK_TAG"] = os.path.abspath(os.path.join(os.path.dirname(environ.get("SCRIPT_FILENAME")) + "/views/stylesheets/"))
	# PATH_INFO contains the path beginning from the app-root url. 	# first part is the controller,  	# second part is the action
	powdict["PATH_INFO"] = environ.get("PATH_INFO")
	powdict["ENVIRON"] = show_environ( environ )
	powdict["DOCUMENT_ROOT"] = environ.get("DOCUMENT_ROOT")
	
	powdict["POW_APP_NAME"] = environ.get("pow.app_name")
	powdict["POW_APP_DIR"] = environ.get("pow.wsgi_dir")
	powdict["FLASHTEXT"] = ""
	
	#output.append( show_environ( output, environ ) )
	
	#
	# get controller and action
	#
	pathdict = get_controller_and_action(environ["PATH_INFO"])
	#(controller,action) = os.path.split(pathinfo)
	
	controller = powdict["CONTROLLER"] = pathdict["controller"]
	action = powdict["ACTION"] = pathdict["action"]
	powdict["PATHDICT"]=pathdict
	if controller == '':
		print "setting controller to user and acitn to list user/list"
		controller = "user"
		action = "list"
		
	# get rid of the first / in front of the controller. string[1:] returns the string from char1 to len(string)
	controller = string.capitalize(controller) + "Controller"
	#output.append("controller:")
	#output.append(controller)
	#output.append("<br>")
	#output.append("action:")
	#output.append(action)
	#output.append("<br>")
	
	#
	# route the request
	#
	#mod = powlib.load_module(controller)
	#mod = __import__("UserController")
	
	#output.append("Mod: " + str(dir(mod)) + "<br>")
	#output.append("Controller: " + str(controller) + "<br>")
	
	aclass = powlib.load_class(controller,controller)
	#output.append("aclass: " + str(dir(aclass)) + "<br>")
	#aclass = powlib.load_class(controller,controller)
	aclass.setCurrentAction(action)
	#output.append(action + "<br>")
	if hasattr( aclass, action ):
		real_action = eval("aclass." + action)
	#output.append("real_action: " + str(real_action) + "<br>")
	
	output.append(real_action(powdict).encode('utf-8'))
	#output.append("dir(powlib): " +str(dir(powlib))+ "<br>")
	#output.append("ende<br>")
	#output.append('</p></body></html>')
	
	#
	# error handling wsgi see:
	#	1. http://www.python.org/dev/peps/pep-0333/#error-handling
	# 	2. 
	
	start_response(status, response_headers)
	return output
		
session_opts = {
	'session.type': 'file',
	'session.data_dir': './db',
	'session.cookie_expires': True,
	'session.auto': True
}

#application= SessionMiddleware(powapp, key='mysession', secret='randomsecret')
application = SessionMiddleware(powapp, session_opts)
#application = powapp
	

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

#from gaesessions import SessionMiddleware

#def webapp_add_wsgi_middleware(app):
#    app = SessionMiddleware(app, cookie_key="a random and long string")
#    return app
	
def main():
#   run_wsgi_app(webapp_add_wsgi_middleware(application))
	run_wsgi_app(application)

if __name__ == "__main__":
    main()