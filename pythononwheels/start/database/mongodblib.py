#
# base connection for TinyDB 
#
from {{appname}}.config import database
from pymongo import MongoClient

conn_str = "mongodb://" + database["mongodb"]["host"] + ":" + str(database["mongodb"]["port"]) + "/"
print(" ... setting it up for mongoDB: " + conn_str)
client = MongoClient(database["mongodb"]["host"], database["mongodb"]["port"])
db = client[database["mongodb"]["dbname"]]
collection=db[database["mongodb"]["dbname"]]


    
