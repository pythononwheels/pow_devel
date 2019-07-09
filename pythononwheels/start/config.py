#
#
# pow settings file
# 
import simplejson as json
import {{appname}}.encoders
import os
import logging
import datetime

server_settings = {
    "protocol"          :   "http://",
    "host"              :   "localhost",
    "port"              :   8080,
    "debug"             :   True,
    "debug_print"       :   True,
    #Logs a stack trace if the IOLoop is blocked for more than s seconds. so 0.050 means 50ms
    "IOLoop.set_blocking_log_threshold" : 0, 
    "logging"           :   True,
    "https"             :   False,
    "template_path"     :   os.path.join(os.path.dirname(__file__), "views"),
    "static_url_prefix" :   "/static/",
    "static_path"       :   os.path.join(os.path.dirname(__file__), "static"),
    "login_url"         :   "/login",
    "xsrf_cookies"      :   False,
    #"log_function"      :   you can give your own log function here.
    "cookie_secret"     :   "{{cookie_secret}}"
}

templates = {
    "template_path"     :   server_settings["template_path"],
    "handler_path"      :   os.path.join(os.path.dirname(__file__), "handlers"),
    "model_path"        :   os.path.join(os.path.dirname(__file__), "models"),
    "stubs_path"        :   os.path.join(os.path.dirname(__file__), "stubs"),
    "views_path"        :   os.path.join(os.path.dirname(__file__), "views")
}

myapp = {
    "app_name"          :   "{{appname}}",
    #                           Format : Content-Type Header
    "supported_formats" :   {   "json" : "application/json", "csv" : "text/csv", 
                                "xml" : "application/xml", "html" : "text/html" },
    "default_format"    :   "json",
    "encoder"           :   {
           "json"   :   {{appname}}.encoders.json_to_json(),
            "csv"   :   {{appname}}.encoders.json_to_csv(),
            "xml"   :   {{appname}}.encoders.json_to_xml()
    },
    "byte_decoding"     :   "utf-8",
    "upload_path"       :   os.path.join(server_settings["static_path"], "upload"), #this is just a demo.
    "page_size"         :   5,
    "enable_auth"       :   False,   # False, simple or custom
    "sql_auto_schema"   :   True,
    "logfile"           :   os.path.join(os.path.dirname(__file__),"pow.log"),
    "logformat"         :   logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    "id_pattern"        :   "[0-9\-a-zA-Z]+",       # the regex used to math IDs in URLs (uuid in this case)
    "date_format"       :   "%Y-%m-%d",
    "datetime_format"       :   "%Y-%m-%d %H:%M:%S",
    "html_datetime_format"  :   "%Y-%m-%dT%H:%M:%S",
    "internal_fields"   :   ["created_at", "last_updated", "_uuid"],  # these are not included in the scaffolded views at all
    "default_rest_route":   "list",
    "list_separator"    :   " ",
    "pwhash_method"     :   "pbkdf2:sha256",      # see: http://werkzeug.pocoo.org/docs/0.14/utils/#module-werkzeug.security
    "simple_conversion":   True
    #"environment"      :   "development"       # set the current environment (also see the db section)
}

BASE_DIR = os.path.dirname(__file__)
database = {
    "default_values": {
        "string"    :   "",
        "integer"   :   0,
        "float"     :   0.0,
        "list"      :   [],
        "boolean"   :   False,
        "datetime"  :   datetime.datetime.utcnow(),
        "dict"      :   {},
        "binary"    :   None

    },
    "sql"   : {
        "loglevel"  :   logging.INFO,
        "yield_per" :   100,
        #
        # this is an example for SQlite
        #
        "type"      :   "sqlite", #or: "db+driver" e.g. => "postgres+psycopg2" ...
        "dbname"    :   os.path.join(BASE_DIR, 'db.sqlite'),   # just a name for non file based DBs
        "host"      :   None,     
        "port"      :   None,     
        "user"      :   None,     
        "passwd"    :   None,
        "enabled"   :   False            
        #
        # this is an example for Postgres (psycopg2 driver) you can use your preferred driver of course 
        #     
        # "type"      :   "postgres+psycopg2",
        # "dbname"    :   "powdb",   
        # "host"      :   "localhost",       
        # "port"      :   5432,   
        # "user"      :   "postgres",
        # "passwd"    :   "postgres",
        # "enabled"   :   False              
        #
        # this is an example for MariaDB / MySQL
        #
        # "type"      :   "mysql+pymysql",
        # "dbname"    :   "test",           # just a name for non file based DBs
        # "host"      :   "127.0.0.1",     
        # "port"      :   3306,     
        # "user"      :   "<you db user here>",
        # "passwd"    :   "<your db pwd here>",
        # "enabled"   :   False              

    },
    "tinydb" : {
        "dbname"    :   os.path.join(BASE_DIR, 'tiny.db'),
        "host"      :   None,       
        "port"      :   None,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   True       
    },
    "mongodb" : {
        "dbname"    :   "testdb",  
        "atlas"     :   False,
        "atlas_cstr":   "",     # usually just copy the Atlas connection string here
        "urlencode" :   False,  # if set to True you need to give usr / pwd below 
        "atlas_user":   "",     # will be urllib.parse.quoted
        "atlas_pwd" :   "",     # will still be raw
        "host"      :   "localhost",       
        "port"      :   27017,   
        "user"      :   None,
        "passwd"    :   None,
        #"indexes"   :   { "collection" : ([("field", pymongo.ASCENDING)], { "unique" : True } )},
        "indexes"   :   {},
        "enabled"   :   False       
    },
    "elastic" : {
        "dbname"    :   "testdb",   # == elasticsearch index 
        "hosts"     :   ["localhost"],       
        "port"      :   9200,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   False       
    }
}

mydash={
    # see: https://dash.plot.ly/getting-started
    "external_stylesheets"  :   ['https://codepen.io/chriddyp/pen/bWLwgP.css']
}

beta_settings = {
    # Beta settings are erxperimental. You can find details for each Beta setting
    # on www.pythononwheels.org/beta
    
    # Name          :    Enabled ?
    "dot_format"    :   True
}

#from handlers.very_raw_own_handler import VeryRawOwnHandler
routes = [
            #(r'.*', VeryRawOwnHandler)
]