from wsgiref.simple_server import make_server

import string
import os.path
import sys
import os
import re
from pprint import pformat
from beaker.middleware import SessionMiddleware
from cgi import parse_qs, escape
import traceback, StringIO
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
import urllib

import powlib


def powapp(environ, start_response):
	
	#print show_environ_cli(environ)
	output = []
	powdict =  {}	
	real_action = None
	
	#
	# relevant parameters have to be defined here
	# (Same as for apache the declarations in the httpd.conf file
	#
	
	# redirect static media from the meta link static to the real source dir
	# advantage is: you can alway refer safely to /static/<something> inside your css o .tmpl
	# files and the real source can be anywhere. sometimes the real static source differs from
	# prod-webserver A to prod-webserver B. with this litte tirck you can leave your links unchanged.
	# for apache the redirection is done in http.conf
	alias_dict ={	
		"/static/css/" :	"./public/stylesheets/",
		"/static/media/":	"./public/media/",
		"/static/scripts/" : "./public/scripts/"
		}
	environ["SCRIPT_FILENAME"] = __file__
	powdict["POW_APP_NAME"] = "PythonOnWheels"
	powdict["POW_APP_URL"] = "www.pythononwheels.org"
	powdict["POW_APP_DIR"] = environ.get("pow.wsgi_dir")
	powdict["ERROR_INFO"] = "Undefined ERROR occured or there is no Error specific info available "
	
	# Get the session object from the environ
	session = environ['beaker.session']
	#TO_DO: set the right status in the end, according to the situatio instead of setting it hard-coded here
	status = '200 OK'
	response_headers = [
		('Content-type', 'text/html')
		]

	
	if not session.has_key('user.id'):
		session['user.id'] = 0
	
	#session.save()
	
	powdict["SESSION"] = session
	
	if is_get_request(environ):
		plist = get_http_get_parameters(environ)
	elif is_post_request(environ):
		plist = get_http_post_parameters(environ)
	else:
		return
	#print show_environ_cli(environ)
	
	powdict["PARAMETERS"] = plist
	
	#
	# handling static files
	#
	
	
	pinfo = environ.get("PATH_INFO")
	pinfo_before = pinfo
	ostr = ""
	
	found_static = False
	for elem in alias_dict:
		if string.find(pinfo,  elem) != -1:
			found_static = True
			pinfo = string.replace(pinfo,elem, alias_dict[elem])
	
	environ["PATH_INFO"] = pinfo
	
	if found_static == True:
		#print "-- Static REQUEST --------------------------------------------------------- "
		non_binary = [".css", ".html",".js",".tmpl"]
		ctype = "UNINITIALIZED"
		ftype = os.path.splitext(pinfo)[1]
		
		if string.lower(ftype) in non_binary:
			infile = open (os.path.normpath(pinfo), "r")
		else:
			infile = open (os.path.normpath(pinfo), "rb")
		ostr = infile.read()
		infile.close()
		#print "file type is: ", ftype, " -> ", ctype
		if string.lower(ftype) == ".gif":
			ctype = "image/gif"
		elif string.lower(ftype) == ".jpg" or string.lower(ftype) ==".jpeg":
			ctype= "image/jpeg"
		elif string.lower(ftype) == ".css":
			ctype = "text/css"
		elif string.lower(ftype) == ".png":
			ctype = "image/png"
		elif string.lower(ftype) ==".js":
			ctype= "application/x-javascript"
		else:
			ctype = "text/html"
		#print "file type is: ", ftype, " responding with type-> ", ctype
		response_headers = [
		('Content-type', ctype )
		]
		start_response(status, response_headers)
		return [ostr]
	print "-- Dynamic REQUEST --------------------------------------------------------- "		
	print "Request: " + environ["REQUEST_METHOD"] + " " + environ["PATH_INFO"] + " " + environ["SERVER_PROTOCOL"] + " " + environ["QUERY_STRING"]	
	print "PATH_INFO before: ", pinfo_before
	print "PATH_INFO after: ", pinfo
		
	if not session.has_key('counter'):
		session['counter'] = 0
	session['counter'] += 1

	powdict["SCRIPT_FILENAME"] = environ.get("SCRIPT_FILENAME")
	powdict["SCRIPT_DIR"] = os.path.dirname(environ.get("SCRIPT_FILENAME"))
	powdict["SCRIPT_VIEWS_DIR"] = os.path.abspath(os.path.join(os.path.dirname(environ.get("SCRIPT_FILENAME")) + "/views/"))
	powdict["STYLESHEET_LINK_TAG"] = os.path.abspath(os.path.join(os.path.dirname(environ.get("SCRIPT_FILENAME")) + "/views/stylesheets/"))
	# PATH_INFO contains the path beginning from the app-root url. 	# first part is the controller,  	# second part is the action
	powdict["PATH_INFO"] = environ.get("PATH_INFO")
	#print os.path.split(powdict["PATH_INFO"])
	powdict["ENVIRON"] = show_environ( environ )
	powdict["DOCUMENT_ROOT"] = environ.get("DOCUMENT_ROOT")
	powdict["FLASHTEXT"] = ""
	#output.append( show_environ( output, environ ) )
	
	#
	# get controller and action
	#
	print "environ[\"PATH_INFO\"] = ", environ["PATH_INFO"]
	pathdict = get_controller_and_action(environ["PATH_INFO"])
	#(controller,action) = os.path.split(pathinfo)
	print "(controller,action) -> ", pathdict
	controller = powdict["CONTROLLER"] = pathdict["controller"]
	action = powdict["ACTION"] = pathdict["action"]
	powdict["PATHDICT"]=pathdict

	#TO_DO: include the real, mod re based routing instead of seting it hard to user/list here.
	if controller == "":
		defroute = powlib.readconfig("pow.cfg","routes","default")
		#print get_controller_and_action(defroute)
		pathdict = get_controller_and_action(defroute)
		#(controller,action) = os.path.split(pathinfo)
		print "(controller,action) -> ", pathdict
		controller = powdict["CONTROLLER"] = pathdict["controller"]
		action = powdict["ACTION"] = pathdict["action"]
		powdict["PATHDICT"]=pathdict

		print "Using the DEFAULT_ROUTE: ",
		print "(controller,action) -> ", pathdict
	
	# get rid of the first / in front of the controller. string[1:] returns the string from char1 to len(string)
	controller = string.capitalize(controller) + "Controller"
	
	#
	# route the request
	#
	aclass = powlib.load_class(controller,controller)
	aclass.setCurrentAction(action)
	#output.append(action + "<br>")
	if hasattr( aclass, action ):
		real_action = eval("aclass." + action)
	#output.append("real_action: " + str(real_action) + "<br>")
	
	output.append(real_action(powdict).encode('utf-8'))
	
	#
	# error handling wsgi see:
	#	1. http://www.python.org/dev/peps/pep-0333/#error-handling
	# 	2. 
		
	start_response(status, response_headers)
	return output
		
session_opts = {
	'session.type': 'file',
	'session.data_dir': './session_data',
	'session.cookie_expires': True,
	'session.auto': True
}

#application= SessionMiddleware(powapp, key='mysession', secret='randomsecret')
application = SessionMiddleware(powapp, session_opts)

def pre_route(path_info):
	# description:
	# Syntax: 	r"URL-Pattern"	:	"Redirection-URL"
	# r"^/user/new*" : "/user/list",
	#	=> matches any line starting with /user/new and redirecting it to /user/list
	#	r"^/([w]+)/([w]+)*" : "/user/list",
	# 	=> matches any /action/controller combination not matched by any of the preceeding ones
	#	 and redirecting it to /user/list. you can also access the groups (by parantheses) by match.group(1)..
	# other example:
	# r"^/user/do_login*" : "/user/list",
	# r"^/user/new\w*" : "/user/list",

	routes = {
		r"^/([w]+)/([w]+)*" : "/user/list",
		r"." : "/app/welcome"
	}
	#print routes
	match = None
	for pattern in routes:
		match = re.search(pattern, inp)
		if match:
			print "matched: ", pattern, " --> ", routes[pattern]
			break
		p = None
		match = None
	
	
def show_environ( environ ):
	ostr = ""
	ostr +=  "<h1>Sorted Keys an Values in <tt>environ</tt></h1>" 
	
	sorted_keys = environ.keys()
	sorted_keys.sort()
	
	for key in sorted_keys:
		ostr += str(key) + " = " + str(environ.get(key)) + "<br>"
		
	return ostr

def show_environ_cli( environ ):
	ostr = ""
	ostr +=  "Sorted Keys an Values in environ:" 
	
	sorted_keys = environ.keys()
	sorted_keys.sort()
	
	for key in sorted_keys:
		ostr += str(key) + " = " + str(environ.get(key)) + powlib.newline
		
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
		val = urllib.unquote_plus(val)
		print "in (get_http_post_parameters)    val=",val , "  newval=", newval
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



if __name__ == "__main__":
	httpd = make_server('', 8080, application)
	print "Serving HTTP on port 8080..."

	# Respond to requests until process is killed
	httpd.serve_forever()

	# Alternative: serve one request, then exit
	#httpd.handle_request()
