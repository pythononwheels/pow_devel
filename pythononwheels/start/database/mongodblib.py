#
# base connection for TinyDB 
#
from {{appname}}.config import database
#from pymongo import MongoClient
import pymongo
import urllib
if not database["mongodb"]["atlas"]:
    # normal mongodb server (local or remote)
    conn_str = "mongodb://" + database["mongodb"]["host"] + ":" + str(database["mongodb"]["port"]) + "/"    
    print(" ... setting it up for mongoDB: " + conn_str)
    client = pymongo.MongoClient(database["mongodb"]["host"], database["mongodb"]["port"])
    #db = client[database["mongodb"]["dbname"]]
    #collection=db[database["mongodb"]["dbname"]]

else:
    # go cloudy &  set it up for atlas use
    if not database["mongodb"]["urlencode"]:
        conn_str = database["mongodb"]["atlas_cstr"]
        print(" ... setting it up for mongoDB Atlas: {}".format( conn_str[conn_str.index(r"@"):] ))
    else:
        conn_str="mongodb+srv://" + urllib.parse.quote(database["mongodb"]["atlas_user"]) + ":" 
        conn_str += database["mongodb"]["atlas_pwd"] + r"@" + database["mongodb"]["atlas_cstr"]
        print(" ... setting it up for mongoDB Atlas: ({}) @{} ".format( 
        database["mongodb"]["atlas_user"], database["mongodb"]["atlas_cstr"] ))
    
    
    client = pymongo.MongoClient(conn_str)

db = client[database["mongodb"]["dbname"]]
collection=db[database["mongodb"]["dbname"]]

    
