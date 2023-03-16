#
# base connection for TinyDB 
#
from {{appname}}.conf.config import database
#from pymongo import MongoClient
import pymongo
import urllib
if not database["mongodb"]["atlas"]:
    # normal mongodb server (local or remote)
    # with user and password
    if database["mongodb"]["user"] and database["mongodb"]["passwd"]:
        conn_str = "mongodb://" + database["mongodb"]["user"] +":" + database["mongodb"]["passwd"] + "@" + database["mongodb"]["host"] + ":" + str(database["mongodb"]["port"]) + "/"
        client = pymongo.MongoClient( 
            host=database["mongodb"]["host"] + ":" + str(database["mongodb"]["port"]),
            username = database["mongodb"]["user"],
            password = database["mongodb"]["passwd"]

        )
    else:
        # without user and password
        conn_str = "mongodb://" + database["mongodb"]["host"] + ":" + str(database["mongodb"]["port"]) + "/"    
        print(" ... setting it up for mongoDB: " + conn_str)
        client = pymongo.MongoClient( 
            host=database["mongodb"]["host"] + ":" + str(database["mongodb"]["port"])    
        )
    #db = client[database["mongodb"]["dbname"]]
    #collection=db[database["mongodb"]["dbname"]]

else:
    # go cloudy &  set it up for atlas use
    if not database["mongodb"]["urlencode"]:
        conn_str = database["mongodb"]["atlas_cstr"]
        #print(" ... setting it up for mongoDB Atlas: {}".format( conn_str[conn_str.index(r"@"):] ))
    else:
        conn_str="mongodb+srv://" + urllib.parse.quote(database["mongodb"]["atlas_user"]) + ":" 
        conn_str += database["mongodb"]["atlas_pwd"] + r"@" + database["mongodb"]["atlas_cstr"]
        print(" ... setting it up for mongoDB Atlas: ({}) @{} ".format( 
            database["mongodb"]["atlas_user"], database["mongodb"]["atlas_cstr"] )
        )
    
    
    client = pymongo.MongoClient(conn_str)

db = client[database["mongodb"]["dbname"]]
collection=db[database["mongodb"]["dbname"]]
    
