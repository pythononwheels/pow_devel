import tornado.web
import tornado.escape
import json
from {{appname}} import config as cfg
from {{appname}}.models.{{dbtype}}.user import User



class BaseHandler(tornado.web.RequestHandler):

    def initialize(self, *args, **kwargs):
        """
            receives the URL dict parameter.
            For PoW RESTroutes this looks like this: (Kwargs)
            { "get" : "some_method" }
            { "http_verb" : "method_to_call", ...}
            { "params" : ["id", "name", ... ]}
        """
        print("  .. in initialize")
        print("  .. .. args: " + str(args))
        print("  .. .. kwargs: " + str(kwargs))
        self.dispatch_kwargs = kwargs
        self.dispatch_args = args
        
        
    def prepare(self):
        """
            Called at the beginning of a request before get/post/etc.
        """
        
        #print(self.request)
        self.uri = self.request.uri
        print("Request:" )
        print(30*"-")
        print(" Mehtod: " + self.request.method)
        print(" URI: " + self.uri)
        print(" Handler: " + self.__class__.__name__)
        # path = anything before url-parameters
        self.path = self.request.uri.split('?')[0]
        print(" path: " + self.path)
        #
        # You can use the before_handler in a local controller to
        # process your own prepare stuff.
        # a common use case is to call: self.print_debug_info().
        # which then applies only to this specific Controller.
        # 
        before_handler = getattr(self, "before_handler", None)
        if callable(before_handler):
            print("calling before_handler for " +  str(self.__class__))
            before_handler()
        self.format = self.get_accept_format()

    
    def get_format_list(self, h=None):
        """
            uses a a header list from self.request.headers.get("Accept")
            to just return the plain formats 
            like: html, xml, xhtml or *
        """
        if not h:
            h = self.request.headers.get("Accept")
        headers_raw = h.split(",")
        print(headers_raw)
        h_final = []
        # example Accept-header: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8 
        for elem in headers_raw:
            # erase everything after ; and +
            try:
                elem = elem[elem.index("/")+1:]
            except:
                pass
            try:
                elem = elem[:elem.index(';')]
            except:
                pass
            try:
                elem = elem[:elem.index('+')]
            except:
                pass
            h_final.append(elem)
        return h_final

    def get_accept_format(self):
        """
            format is either added as accept header format 
            or as .format to the path
            or default_format
            example: /post/12.json (will return json)
        """
        # Try the Accept Header first:
        format = None
        accept_header = self.request.headers.get("Accept", None)
        if accept_header:
            format_list = self.get_format_list(accept_header)
            print("formats from Accept-Header: " + str(format_list))
            # returns the first matched format from ordered Accept-Header list.
            for fo in format_list:
                if fo in cfg.myapp["supported_formats"]:
                    return fo
        
        if cfg.beta_settings["dot_format"]:
            # try the .format
            if len (self.path.split(".")) > 1:
                format = self.path.split(".")[-1]
        
        
        if format == None:
            # take the default app format (see config.cfg.myapp)
            format = cfg.myapp["default_format"]
        
        if format in cfg.myapp["supported_formats"]:
            return format
        else:
            print("format error")
            return self.error(
                    message="Format not supported. (see data.format)",
                    data={
                        "format was" : format,
                        "supported_formats" : cfg.myapp["supported_formats"]
                    }
            )
                
    #
    # GET
    #
    # routes have the form: 
    # ( r"/" + action + r"/" + str(api) + r"/(?P<id>.+)/edit/?" , { "get" : "edit", "params" : ["id"] }),
    # or
    # @app.add_route2("/thanks/*", dispatch={"get": "_get"} )
    def get(self, *args, **params):
        #url_params=self.get_arguments("id")
        print(" ----> GET / BaseHandler")
        print("  .. params : " + str(params))
        print("  .. args : " + str(args))
        print("  .. self.dispatch_kwargs : " + str(self.dispatch_kwargs))
        if self.dispatch_kwargs.get("get", None) != None:
            try:
                # this is the view that will be rendered by success or error,
                # if the format is .html
                # rule: handlerName_methodName
                self.view = self.dispatch_kwargs.get("get", None)

                print("  .. Trying to call handler method: " + self.dispatch_kwargs.get("get") )
                f=getattr(self, self.dispatch_kwargs.get("get"))
                print("  .. trying to call: " + str(f))
                if callable(f):
                    # call the given method
                    return f(*args, **params)
            except TypeError as e:
                self.application.log_request(self, 
                    message=str(e))
                self.error(
                    message=str(e),
                    data = { "request" : str(self.request)},
                    http_code = 405
                )
        else:
            self.error(
                message=" HTTP Method: GET not supported for this route. ",
                data = { "request" : str(self.request )},
                http_code = 405
                )

        #self.write(str(self.request))
    
    #
    # POST   /items     #=> create
    #
    def post(self):
        print(" ---> PUT / BaseHandler")
        print("  .. params : " + str(params))
        print("  .. args : " + str(args))
        print("  .. self.dispatch_kwargs : " + str(self.dispatch_kwargs))
        if self.dispatch_kwargs.get("get", None):
             self.error(
                message=" HTTP Method: GET not supported for this route. ",
                data = { "request" : str(self.request )},
                http_code = 405
                )
        data = tornado.escape.json_decode(self.request.body)
        return self.create(data)

    #
    # PUT    /items/1      #=> update
    #
    def put(self, **params):
        #data = tornado.escape.json_decode(self.request.body)
        try:
            p1 = params.get("param1", None)
            int(p1)
            # if param1 is an integer we call update
            return self.update(p1)
        except ValueError:
            return self.error(500, params, "HTTP/UPDATE needs an ID. ID must be an int")
    
    #
    # DELETE /items/1      #=> destroy
    # 
    def delete(self, **params):
        #data = tornado.escape.json_decode(self.request.body)
        try:
            p1 = params.get("param1", None)
            int(p1)
            # if param1 is an integer we call update
            return self.destroy(p1)
        except ValueError:
            return self.error(500, params, "HTTP/UPDATE needs an ID. ID must be an int")


    def success(self, message=None, data=None, succ=None, prev=None,
        http_code=200, format=None, encoder=None):
        """
            returns data and http_code.
            data will be converted to format.  (std = json)
            for other formats you have to define an encoder in config.py
            (see json as an example)
        """
        self.application.log_request(self, message="base.success:" + message)
        self.set_status(http_code)
        if not format:
            format = self.format
        if not format:
            format = cfg.myapp["default_format"]
        if format.lower() == "html":
            # special case where we render the classical html templates
            viewname = self.__class__.__name__ + "_" + self.view + ".tmpl"
            if self.view is not None:
                self.render( viewname, data=self.json_result_to_object(data), message=message, handler_name = self.__class__.__name__ )
            else:
                self.error(message="Sorry, View: " + viewname +  " can not be found.", 
                    format=format, data=data)
        if encoder:
            encoder = encoder
        else:
            encoder = cfg.myapp["encoder"][format]
        self.write(encoder.dumps({
            "status"    : http_code,
            "message"   : message,
            "data"      : data,
            "next"      : succ,
            "prev"      : prev
        }))
        self.finish()

    def error(self, message=None, data=None, succ=None, prev=None,
        http_code=500, format=None, encoder=None):
        
        self.application.log_request(self, message="base.error:" + message)
        self.set_status(http_code)
        
        if not format:
            format = self.format
        if not format:
            format = cfg.myapp["default_format"]
        if format.lower() == "html":
            self.render("error.tmpl", data=data, message=message)
        if encoder:
            encoder = encoder
        else:
            encoder = cfg.myapp["encoder"][format]
        self.write(encoder.dumps({
            "status"    : http_code,
            "data"      : data,
            "error"     : {
                "message"   : message
                },
            "next"      : succ,
            "prev"      : prev
        }))
        self.finish()

    def write_error(status_code, **kwargs):
        """
            write_error may call write, render, set_header, etc to produce 
            output as usual.
            If this error was caused by an uncaught exception 
            (including HTTPError), an exc_info triple will be available as 
            kwargs["exc_info"]. Note that this exception may not be the 
            âcurrentâ exception for purposes of methods like sys.exc_info() 
            or traceback.format_exc.
        """
        #if status_code == 404:
        return self.render("404.tmpl")

