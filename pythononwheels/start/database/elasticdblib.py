#
# base connection for Elasticsearch
#
from {{appname}}.config import database
from elasticsearch import Elasticsearch
import requests
#from elasticsearch_dsl.connections import connections

elastic = database.get("elastic", None)

#connections.create_connection(hosts= elastic["hosts"], timeout=20)

es=None
if elastic:
    es = Elasticsearch( [{ 'host': elastic["hosts"][0], 'port': elastic["port"]}] )
    #es = Elasticsearch()
    dbname=elastic.get("dbname", None)
if es:
    print(" ... setting it up for Elasticsearch: " + str(es))
    res = requests.get("http://" + elastic["hosts"][0] + ":" + str(elastic["port"]))
    print(str(res.content))
else:
    raise Exception("I had a problem setting up a connection to Elasticsearch")
    

    
# Basic elastic  terminology:
#--------------------------------
# index ~= database
# type ~= table 
# document = yes, what you thought ;)

# create the index, ignore if the index (~= db) already exists
es.indices.create(index=elastic["dbname"], ignore=400)