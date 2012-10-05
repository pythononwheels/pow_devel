#
# Date: 24.1.2012
# Author: khz
# module with the shared functions of pow_router and simple_server
#

import sys
import os
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
import urllib
import re
import cgi
import string
import sqlalchemy.types
import powlib

#
# session management default values.
#
session_opts = {
    'session.type': 'file',
    'session.data_dir': './sessions',
    'session.cookie_expires': True,
    'session.auto': True
}

def log( instr ):
    print >> environ['wsgi.errors'], instr
    return

def set_text_or_binary_form_data(model, powdict, bin_data_path="/public/img"):
    """
        iterates over all parameters in the current requests and updates
        the according model fields.
        Handles text and binary data coorectly. Text is directly stored in the
        models attribute. For binary data the file is stored in the given path and 
        the link is stored in the model attribute.
        If binary_data is expected depends on the models.attribute type, NOT on the submitted
        data.
        @param model:            the Model
        @param powdict:          the powdict of the current request
        @param bin_data_path:    path where the binary data will be stored.
        @returns:                the updated model. You need to call model.update 
                                 (or model.create) afterwards, yourself to really update the db.
    """ 
    dict = powdict["REQ_PARAMETERS"]
    for key in dict:
        curr_type = model.get_column_type(key)
        if curr_type == type(sqlalchemy.types.BLOB()) or curr_type == type(sqlalchemy.types.BINARY()):
            #ofiledir  = os.path.normpath(bin_data_path)
            #print "key: ", key
            if form_has_binary_data( key, dict, bin_data_path):
                # if form contains file data AND file could be written, update model
                model.set(key, dict[key].filename )   
            else:
                # dont update model
                print " ##### ________>>>>>>>   BINARY DATA but couldnt update model"
        else:
            model.set(key, dict[key])
    return model


def get_form_binary_data( form_fieldname, dict, ofiledir ):
    return form_has_binary_data( form_fieldname, dict, ofiledir )

def form_has_binary_data( form_fieldname, dict, ofiledir ):
    """ safely checks if a given form field has binary data attached to it
        and safes it into the given filename. Often used for html form <input type="file" ...>
    """
    if dict.has_key(form_fieldname):
        try:
            #print dir(dict[form_fieldname])
            #print dict[form_fieldname].__dict__.viewkeys()
            data = dict[form_fieldname].file.read()
            #ofiledir = os.path.normpath("./public/img/blog/")
            ofilename = os.path.join(ofiledir, dict[form_fieldname].filename)
            ofile = open( ofilename , "wb")
            ofile.write(data)
            ofile.close()
            return True
        except AttributeError:
            # no image data
            return False
    return False

def pre_route(path_info):
    # description:
    # Syntax:     r"URL-Pattern"    :    "Redirection-URL"
    # r"^/user/new*" : "/user/list",
    #    => matches any line starting with /user/new and redirecting it to /user/list
    #    r"^/([w]+)/([w]+)*" : "/user/list",
    #     => matches any /action/controller combination not matched by any of the preceeding ones
    #     and redirecting it to /user/list. you can also access the groups (by parantheses) by match.group(1)..
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

   
def get_http_post_parameters_new( environ ):
    # see: http://www.wsgi.org/en/latest/specifications/handling_post_forms.html?highlight=post
    # form.getvalue('name'):
    assert is_post_request(environ)
    input = environ['wsgi.input']
    post_form = environ.get('wsgi.post_form')
    print "in get_http_post_parameters_new( environ ):"
    if (post_form is not None
        and post_form[0] is input):
        return post_form[2]
    # This must be done to avoid a bug in cgi.FieldStorage
    environ.setdefault('QUERY_STRING', '')
    fs = cgi.FieldStorage(fp=input,
                          environ=environ,
                          keep_blank_values=1)
    return fs




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
        #content_type = environ.get('CONTENT_TYPE', 'application/x-www-form-urlencoded')
        #return (content_type.startswith('application/x-www-form-urlencoded' or content_type.startswith('multipart/form-data')))

def is_get_request( environ ):
    if environ['REQUEST_METHOD'].upper() != 'GET':
        return False
    else:
        return True
    
def get_controller_and_action(pi="/"):
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

#
# reference: http://pylonsbook.com/en/1.1/the-web-server-gateway-interface-wsgi.html
# also see: http://svn.python.org/projects/python/branches/release25-maint/Lib/cgitb.py
import cgitb
import sys
from StringIO import StringIO

class Middleware(object):
    def __init__(self, app):
        self.app = app

    def format_exception(self, exc_info):
        dummy_file = StringIO()
        # see: ViewClass in cgitb.Hook
        # here: http://wstein.org/home/wstein/www/home/mhansen/moin-1.7.2/src/MoinMoin/support/cgitb.py
        hook = cgitb.Hook(file=dummy_file)
        hook(*exc_info)
        return [dummy_file.getvalue()]

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except:
            exc_info = sys.exc_info()
            start_response(
            '500 Internal Server Error,',
            [('content-type', 'text/html')],
            exc_info 
            )
            return self.format_exception(exc_info)
