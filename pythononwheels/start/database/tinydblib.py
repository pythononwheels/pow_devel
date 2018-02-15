#
# base connection for TinyDB 
#
from {{appname}}.config import database
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from {{appname}}.models.tinydb.serializer import DateTimeSerializer


tinydb = database.get("tinydb", None)

serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

if tinydb:
    conn_str = tinydb["dbname"]
    print(" ... setting it up for tinyDB: " + conn_str)
    tinydb = TinyDB(conn_str, storage=serialization)
else:
    raise Exception("I had a problem setting up tinyDB")
    

    
