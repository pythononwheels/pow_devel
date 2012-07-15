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



def powapp_router(environ, start_response):
	#
	# set the include path according to the wsgi basepath of the script.
	basepath = environ.get("pow.wsgi_dir")
	sys.path.append(os.path.normpath(basepath + "/lib"))
	sys.path.append(os.path.normpath(basepath + "/controllers"))
	sys.path.append(os.path.normpath(basepath + "/models"))
	import powlib
	import pow_web_lib
	
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
		plist = pow_web_lib.get_http_get_parameters(environ)
	elif is_post_request(environ):
		plist = pow_web_lib.get_http_post_parameters(environ)
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
	pathdict = pow_web_lib.get_controller_and_action(environ["PATH_INFO"])
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


#application= SessionMiddleware(powapp, key='mysession', secret='randomsecret')
application = SessionMiddleware(powapp_router, pow_web_lib.session_opts)

	

