#
# base connection for TinyDB 
#
from {{appname}}.conf.config import database
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from {{appname}}.models.tinydb.serializer import DateTimeSerializer


# tinydb = database.get("tinydb", None)

# serialization = SerializationMiddleware()
# serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

# if tinydb:
#     conn_str = tinydb["dbname"]
#     print(" ... setting it up for tinyDB: " + conn_str)
#     tinydb = TinyDB(conn_str, storage=serialization)
# else:
#     raise Exception("I had a problem setting up tinyDB")

from {{appname}}.lib.powlib import Dbinfo

def generate_connection(db_conf=None):
    """
        create a connection from th given conf
        or from config.py (if db_conf == None)
    """
    if db_conf == None:
        tinydb = database.get("tinydb", None)        
    else:
        tinydb = db_conf
    
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

    if tinydb:
        conn_str = tinydb["dbname"]
        #print(" ... setting it up for tinyDB: " + conn_str)
        tdb=  TinyDB(conn_str, storage=serialization)
        return Dbinfo(db=tdb, collection=None)
    else:
        raise Exception("I had a problem setting up tinyDB")
