import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import os.path
import sys
from werkzeug.routing import Rule, Map, _rule_re

import {{appname}}.config as cfg
from {{appname}}.powlib import merge_two_dicts
from {{appname}}.database.sqldblib import Base, Session, engine
from {{appname}}.config import myapp
from {{appname}}.config import routes
from tornado.log import access_log
import logging
import datetime
from logging.handlers import RotatingFileHandler

#
# global logger settings
#
formatter = myapp["logformat"]
log_handler = logging.FileHandler(os.path.abspath(os.path.normpath(myapp["logfile"])))
#log_handler.setLevel(db_handler_log_level)
log_handler.setFormatter(formatter)

#
# analytics_log_handler 
#
LOG_FILENAME = './pow_analytics.log'

# Set up a specific logger with our desired output level
analytics_logger = logging.getLogger('PowAnalyticsLogger')
analytics_logger.setLevel(logging.INFO)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20000, backupCount=5)

analytics_logger.addHandler(handler)

#
# the direct method decorator
# see: https://stackoverflow.com/questions/2366713/can-a-python-decorator-of-an-instance-method-access-the-class
#
# marks a method as routed and injects and attribute (route) which
# has all the necessary routing parameters (route, dispatch, pos)
# dispatch is a list (not a dict in this case) since the method doesnt have to be
# explicitly defined twice.
#
# the actual routes are added by the class decorator @app.route which
# iterates over all handler-class methods and adds routes for all marked methods.
#
# see the route method(decorator) in the Application class below.
def route(route, dispatch=[], params=[], pos=-1):
    def decorator(method):
        #print("decorating method route: {} : {} : {}".format(route, str(dispatch), method))
        method.routed=True
        method.route={
            "route"     : route,
            "dispatch"  : dispatch,
            "params"    : params, 
            "pos"       : pos
        }
        return method
    return decorator

class Application(tornado.web.Application):
    #
    # handlers class variable is filled by the @add_route decorator.
    # merged with the instance variable in __init__
    # so classic routes and @add_routes are merged.
    #
    handlers=[]

    #routing list to handle absolute route positioning
    handlers_tmp = []

     
    def __init__(self):
        self.handlers = routes
        # importing !"activates" the add_route decorator
        self.import_all_handlers()
        h=getattr(self.__class__, "handlers", None)
        #self.handlers+=h

        # use the absolute positioning routing table
        
        #print(list(reversed(sorted(htmp, key=get_key))))
        # just for route ordering. (sotrted)
        def get_key(item):
            return item[1]
        ## working version:
        #self.show_positioned_routes( list(reversed(sorted(h, key=get_key))) )
        #hordered=[x[0] for x in reversed(sorted(h, key=get_key))]
        ## end!
        hordered = self.order_routes(h)
        #print(str(hordered))
        self.handlers+=hordered

        # merge two dictionaries:  z = { **a, **b }
        # http://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
        settings = merge_two_dicts( dict(
            template_path=os.path.join(os.path.dirname(__file__), cfg.server_settings["template_path"]),
            static_path=os.path.join(os.path.dirname(__file__), cfg.server_settings["static_path"])
        ) , cfg.server_settings)
        super(Application, self).__init__(self.handlers, **settings)
        self.Session = Session
        self.engine = engine
        self.Base = Base
    
    
    def order_routes(self, routes):
        """ order the routes.
            1) if no pos is given, routes are appended in the order they "arrived"
            2) positioned routes are inserted in this list afterwords.
            3) the list is reversed (so pos=0 will be the last routes, pos=1 the second last ...)
                You'll most probably add something like:
                    @app.add_route("/", pos=1) to IndexHandler 
                and:
                    @app.add_route(".*", pos=0) to yur ErrorHandler to catch all unhandled routes.
        """
        
        def get_key(item):
            return item[1]
        hordered = []
        tmp=[]
        for elem in routes:
            if elem[1] == -1:
                hordered.append((elem[0], len(hordered)))
            else:
                tmp.append(elem)
        tmp=sorted(tmp, key=get_key)
        for elem in tmp:
            hordered.insert(elem[1], (elem[0], elem[1]))

        #self.show_positioned_routes(hordered)
        #hordered=list(sorted(hordered, key=get_key))
        hordered=reversed(hordered)
        hordered=[x[0] for x in hordered]
        
        return hordered


    def log_request(self, handler, message=None):
        """ 
            custom log method
            access_log is importef from tornado.log (http://www.tornadoweb.org/en/stable/_modules/tornado/log.html)
            access_log = logging.getLogger("tornado.access")
            you can define you own log_function in config.py server_settings
        """
        #super().log_request(handler)
        if "log_function" in self.settings:
            self.settings["log_function"](handler)
            return
        if handler.get_status() < 400:
            log_method = access_log.info
        elif handler.get_status() < 500:
            log_method = access_log.warning
        else:
            log_method = access_log.error
        request_time = 1000.0 * handler.request.request_time()
        #log_method("%d %s %.2fms", handler.get_status(),
        #           handler._request_summary(), request_time)
        log_method("%s %d %s %.2fms %s", handler.request.remote_ip, handler.get_status(),
                handler._request_summary(), request_time, datetime.datetime.utcnow().strftime(myapp["datetime_format"]) 
            )
        if message:
            log_method("%s %d %s %s", 
                handler.request.remote_ip, 
                handler.get_status(), 
                str(message), 
                datetime.datetime.utcnow().strftime(myapp["datetime_format"])  
            )

    def log(self, message, status="INFO"):
        """ 
            custom log method
            access_log is importef from tornado.log (http://www.tornadoweb.org/en/stable/_modules/tornado/log.html)
            access_log = logging.getLogger("tornado.access")
            you can define you own log_function in config.py server_settings

            status can be: INFO, WARN(INF), ERFR(OR)
        """
        
        if "log_function" in self.settings:
            self.settings["log_function"](status, message)
            return
        
        if status.lower()== "warn" or status == "warning":
            log_method = access_log.warning
            status="WARNING"

        elif status.lower() == "error" or status == "err": 
            log_method = access_log.error
            status="ERROR"
            #log_method("%s %d %s", handler.request.remote_ip, handler.get_status(), str(message))
            log_method("%s %s %s", 
                status, 
                message, 
                datetime.datetime.utcnow().strftime(myapp["datetime_format"]))
        else:
            log_method = access_log.info
            status="INFO"
        
        self.log("You have to give a message when using the application.log() function")
        #raise Exception("You have to give a message when using the application.log() function")
    
    def log_analytics(self, request):
        """ 
            logs the request's:
                 remote IP,
                 URI
                 timestamp 
                 for statistical reasons. So you have a basic analytics without installing
                 the BIg G ;)
        """
        log_method=analytics_logger.info 
        x_real_ip="None"
        try:
            x_real_ip = request.headers.get("X-Real-IP")
        except:
            pass
        log_method("%s %s %s %s %.2fms %s", 
                request.remote_ip, 
                x_real_ip,
                request.method,
                request.uri, 
                1000.0 * request.request_time(),
                datetime.datetime.utcnow().strftime(myapp["datetime_format"])
                )
            
    def import_all_handlers(self):
        """
            imports all handlers to execue the @add_routes decorator.
        """
        import os
        exclude_list=["base", "powhandler"]

        #
        # the list of handlers (excluding base. Add more you dont want
        # to be loaded or inspected to exclude_list above.)
        #
        mods=[]
        module_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'handlers'))
        #print("importing handlers from: " + module_path)
        for mod in os.listdir( module_path ):
            mod = mod.split(".")[0]
            if not mod.startswith("_") and not mod in exclude_list:
                #print("  now processing: " + str(mod))
                mods.append(mod)
                
        #print("mods: " + str(mods))
        class_list = []
        # load all the models from their modules (mods)
        #print(str(mods))
        import importlib
        for m in mods:
            #print("importing: " + '{{appname}}.handlers.' + m)    
            try:
                mod = importlib.import_module('{{appname}}.handlers.' + m)
            except:
                pass
            #print(dir(mod))

    def show_positioned_routes(self, routes):
        """
            show all current routes.
        """
        print(55*"-")
        print("  Positioned Routes:")
        print(55*"-")
        for elem in routes:
            print(str(elem))

    def show_routes(self):
        """
            show all current routes.
        """
        routelist= [(handler.regex.pattern, handler.handler_class) for handler in self.handlers[0][1]]
        print(55*"-")
        print("  Routing table (order matters) :")
        print(55*"-")
        for elem in routelist:
            print('{0:<20} {1:<30} '.format(elem[0], str(elem[1])))

    
    #
    # the RESTful route decorator v2
    # with dedicated routes. One per default action
    #
    def add_rest_routes(self, route, api=None, pos=-1):
        """
            cls is the class that will get the RESTful routes
            it is automatically the decorated class
            self in this decorator is Application
            api will insert the given api version into the route (e.g. route=post, api=1.0)
            /post/1.0/**all restroutes follow this pattern
            1  GET    /items            #=> index (list)
            2  GET    /items/1          #=> show
            3  GET    /items/new        #=> new
            4  GET    /items/1/edit     #=> edit
            5  GET    /items/page/0     #=> page  
            6  PUT    /items/1          #=> update
            7  POST   /items            #=> create
            8  DELETE /items/1          #=> destroy
        """
        def decorator(cls):
            # parent is the parent class of the relation
            #print("in add_rest_routes")
            cls_name = cls.__name__.lower()
            #print(cls_name)
            
            action_part = route
            if api:
                action_part + r"/" + str(api)
            
            # set the base_path fpr rest routes. So you can reference it in templates.
            # see: handlers/base.success(...)
            setattr(cls, "base_route_rest", action_part)

            ID_PATTERN = cfg.myapp["id_pattern"]
            routes = [
                # tuple (http_method, route, { http_method : method_to_call_in_handler, .. })
                ( r"/" + action_part + r"/search/?" , { "get" : "search" }),
                ( r"/" + action_part + r"/list/?",  {"get" : "list"}),
                ( r"/" + action_part + r"/new/?",  {"get" : "new"}),
                ( r"/" + action_part + r"/page/?(?P<page>"+ID_PATTERN+")?/?", { "get" : "page", "params" : ["page"] }),
                ( r"/" + action_part + r"/show/?(?P<id>"+ID_PATTERN+")?/?",  { "get" : "show" , "params" : ["id"]} ),
                ( r"/" + action_part + r"/(?P<id>"+ID_PATTERN+")/edit/?" , { "get" : "edit", "params" : ["id"] }),
                ( r"/" + action_part + r"/(?P<id>"+ID_PATTERN+")?/?", 
                     { "get" : "show" , "put" : "update", "delete" : "destroy", "params" : ["id"]} ),
                ( r"/" + action_part + r"/?", { "get" : cfg.myapp["default_rest_route"], "post" : "create", "put" : "update", "delete" : "destroy" })                
            ]
            routes.reverse()
            # BETA: Add the .format regex to the RESTpattern   
            # this makes it possible to add a .format at an URL. Example /test/12.json (or /test/12/.json)
            if cfg.beta_settings["dot_format"]:
                routes = [(x[0]+ r"(?:/?\.\w+)?/?", x[1]) for x in routes]  
            #print("added the following routes: " + r)
            handlers=getattr(self.__class__, "handlers", None)
            try:
                for elem in routes:
                    handlers.append( ((elem[0],cls, elem[1]), pos) )
            except Exception as e:
                print("Error in add_rest_routes")
                raise e
            print("ROUTING: RESTful ROUTE (+): " + cls.__name__ +  " as /" + action_part)
            #print(dir())
            return cls
        return decorator
    
    #
    # direct method routing
    # decorate methods directly like this:
    # @route( "/route/here/<int:val>", dispatch=[ "HTTP_VERB", "HTTP_VERB2" ], pos=num )
    #
    # then decorate the class with @app.route()
    def make_routes(self):
        """
            the app.route decorator collects all marked methods and
            creates the actual routes.
            The methods are marked using the @route() decorator. (see above)
        """
        def decorator(cls):
            #
            # first, check all methods for the method decorator mark
            #
            #for name, method in cls.__dict__.iteritems():
            #    if hasattr(method, "has_route"):
            #        # do something with the method and class
            #        print("Method route: {}, {}".format(name, str(cls)))
            # parent is the parent class of the relation
            cls_name = cls.__name__.lower()
            #print("in @app.route")
            for name, method in cls.__dict__.items():
                if hasattr(method, "routed"):
                    #print(30*"--")
                    #print("  routed Method  ")    
                    #print("  * name: {}, method: {}". format(name,method))
                    #print("  ** routes: {}".format(str(method.route)))
                    #print(30*"--")
                    # Create the route parameters from the route marked by @route
                    # route, dispatch, pos
                    route=method.route.get("route", None)
                    # construct the dispatch dict from the http_vers list
                    # ["get"] => 
                    #       { "get" : method_name }
                    #
                    dispatch = {key: name for key in method.route.get("dispatch", [])}
                    pos = method.route.get("pos", -1)
                    # now just do the same as for the class decorator
                    handlers=getattr(self.__class__, "handlers", None)
                    if _rule_re.match(route):
                        ########################################
                        # new style Werkzeug route
                        ########################################
                        r=Rule(route, endpoint=cls_name)
                        m = Map()
                        m.add(r)
                        c=m.bind(cfg.server_settings["host"]+":"+cfg.server_settings["host"], "/")
                        r.compile()
                        #print("r1: " +  str(r._regex.pattern))
                        pattern = r._regex.pattern.replace('^\|', "")
                        #print("r1: " +  str(pattern))
                        fin_route = pattern
                        # convert the HTTP Methods in dispatch to lowercase
                        dispatch_lower=dict((k.lower(), v) for k,v in dispatch.items())
                        route_tuple = (fin_route,cls, dispatch_lower)
                        handlers.append((route_tuple,pos))
                    else:
                        ###################################
                        #  old style regex route
                        ###################################

                        # BETA: this regex is added to every route to make 
                        # 1.the slash at the end optional
                        # 2.it possible to add a .format paramter.
                        # Example: route = /test -> also test.json will work
                        # Example: route = /test/([0-9]+) -> also /test/12.xml will work 
                        if cfg.beta_settings["dot_format"]:
                            fin_route = route  + r"(?:/?\.\w+)?/?"
                        else:
                            fin_route = route
                        # convert the HTTP Methods in dispatch to lowercase
                        dispatch_lower=dict((k.lower(), v) for k,v in dispatch.items())
                        route_tuple = (fin_route,cls, dispatch_lower)
                        #route_tuple = (fin_route,cls, dispatch)
                        handlers.append((route_tuple,pos))
                    #print("handlers: " + str(self.handlers))
                    #print("ROUTING: added route for: " + cls.__name__ +  ": " + route + " -> " + fin_route +  " dispatch")
                    #print("ROUTING: METHOD ROUTE (+) : handler: {}, route: {}, fin_route: {}, dispatch(lower): {} ".format( 
                    #    str(cls.__name__), route, fin_route, str(dispatch_lower)))
                    print("ROUTING: METHOD ROUTE (+) : route: {:30} handler: {:20} dispatch: {:15} ".format( 
                        route, str(cls.__name__), str(list(dispatch_lower.keys()))))
            return cls
        return decorator
    
    # 
    #
    # the direct route decorator
    #
    def add_route(self, route, dispatch={}, pos=-1):
        """
            cls is the class that will get the given route / API route
            cls is automatically the decorated class
            self in this decorator is Application
            this will take a 1:1 raw tornado route

            for regex with optional parts that are dropped 
            (Non copturing like: (?: ...) see:
            http://stackoverflow.com/questions/9018947/regex-string-with-optional-parts
        """
        def decorator(cls):
            """
                the actual decorator
            """
            cls_name = cls.__name__.lower()
            handlers=getattr(self.__class__, "handlers", None)
            if _rule_re.match(route):
                ########################################
                # new style Werkzeug route
                ########################################
                r=Rule(route, endpoint=cls_name)
                m = Map()
                m.add(r)
                c=m.bind(cfg.server_settings["host"]+":"+cfg.server_settings["host"], "/")
                r.compile()
                #print("r1: " +  str(r._regex.pattern))
                pattern = r._regex.pattern.replace('^\|', "")
                #print("r1: " +  str(pattern))
                fin_route = pattern
                # convert the HTTP Methods in dispatch to lowercase
                dispatch_lower=dict((k.lower(), v) for k,v in dispatch.items())
                route_tuple = (fin_route,cls, dispatch_lower)
                handlers.append((route_tuple,pos))
            else:
                ###################################
                #  old style regex route
                ###################################

                # BETA: this regex is added to every route to make 
                # 1.the slash at the end optional
                # 2.it possible to add a .format paramter.
                # Example: route = /test -> also test.json will work
                # Example: route = /test/([0-9]+) -> also /test/12.xml will work 
                if cfg.beta_settings["dot_format"]:
                    fin_route = route  + r"(?:/?\.\w+)?/?"
                else:
                    fin_route = route
                # convert the HTTP Methods in dispatch to lowercase
                dispatch_lower=dict((k.lower(), v) for k,v in dispatch.items())
                route_tuple = (fin_route,cls, dispatch_lower)
                #route_tuple = (fin_route,cls, dispatch)
                handlers.append((route_tuple,pos))
            #print("handlers: " + str(self.handlers))
            #print("ROUTING: added route for: " + cls.__name__ +  ": " + route + " -> " + fin_route +  " dispatch")
            #print("ROUTING:  CLASS ROUTE (+) : handler: {}, route: {}, fin_route: {}, dispatch(lower): {} ".format( 
            #   str(cls.__name__), route, fin_route, str(dispatch_lower)))
            print("ROUTING:  CLASS ROUTE (+) : route: {:30} handler: {:20} dispatch: {:15} ".format( 
               route, str(cls.__name__), str(list(dispatch_lower.keys()))))
            return cls
        return decorator
    
   
app=Application()