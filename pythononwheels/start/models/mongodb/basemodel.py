from {{appname}}.database.mongodblib import db, client, collection
from {{appname}}.powlib import pluralize
import datetime
import xmltodict
import simplejson as json
import datetime, decimal
from {{appname}}.config import myapp
from {{appname}}.powlib import merge_two_dicts
from {{appname}}.encoders import pow_json_serializer
from {{appname}}.models.modelobject import ModelObject
#from bson.json_util import dumps
import bson
import pymongo
import uuid

class MongoBaseModel(ModelObject):
    """
        The Raw BaseModel Class
    """    

    basic_schema = {
        "id"    :   { "type" : "string", "default" : None },
        "created_at"    : { "type" : "datetime", "default" : None },
        "last_updated"    : { "type" : "datetime", "default" : None },
    }
    table = collection
    table.create_index([('id', pymongo.ASCENDING)], unique=True)

    def init_on_load(self, *args, **kwargs):
        """
            basic setup for all mongoDB models.
        """
        self.tablename = pluralize(self.__class__.__name__.lower())
        self.table = self.__class__.table
        self._id = None
        #create an index for our own id field.
        
        #
        # if there is a schema (cerberus) set it in the instance
        #
        if "schema" in self.__class__.__dict__:
            #print(" .. found a schema for: " +str(self.__class__.__name__) + " in class dict")
            self.schema = merge_two_dicts(
                self.__class__.__dict__["schema"],
                self.__class__.basic_schema)
            #print("  .. Schema is now: " + str(self.schema))

        # setup  the instance attributes from schema
        for key in self.schema.keys():
            if self.schema[key].get("default", None) != None:
                setattr(self,key,self.schema[key].get("default"))
                self.schema[key].pop("default", None)
            else:
                #print("no default for: " + str(self.schema[key]))
                setattr(self, key, None)
                    
        #
        # setup values from kwargs or from init_from_<format> if format="someformat"
        # example: m = Model( data = { 'test' : 1 }, format="json")
        # will call m.init_from_json(data)
        #
        if "format" in kwargs:
            # set the format and call the according init_from_<format> method
            # which initializes the instance with the given vaules (from data)
            # e.g. Model(format=json, data={data})
            f = getattr(self, "init_from_" + kwargs["format"], None)
            if f:
                f(kwargs)
        else:
            # initializes the instanmce with the given kwargs values:
            # e.g.: Model(test="sometext", title="sometitle")
            for key in kwargs.keys():
                #if key in self.__class__.__dict__:
                if key in self.schema:
                    setattr(self, key, kwargs[key])
                           
    #
    # These Mehtods should be implemented by every subclass
    # 
    def to_json(self, res):
        """ just dump to json formatted string
            parameter:  res must be pymongo cursor. 
                        Example: res = self.table.find() 
        """
        return bson.json_util.dumps(list(cursor))

    def json_result_to_object(self, res):
        """
            returns a list of objects from a given json list (string) 
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
    def result_to_object(self, res):
        """ 
            returns a list of models from a given cursor.
            parameter:  res must be pymongo cursor. 
                        Example: res = self.table.find() 
        """
        return [x.init_from_dict() for x in list(res)]

    def print_full(self):
        """ Subclasses should overwrite this Method. 
            prints every attribute including related objects in FULL
            lenghty but you see everything.
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def json_load_from_db(self, data, keep_id=False):
        """  refresh the object from db and return json """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def print_db_schema(self):
        """ Subclasses should overwrite this Method. 
            Shows the schema as returned by the db
        """ 
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def get_relationships(self):
        """ Subclasses should overwrite this Method. 
            Shows all related classes
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def get_relations(self):
        """ Subclasses should overwrite this Method. 
            Shows all related classes
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def create_table(self):
        """
            create the physical table in the DB
        """
        raise NotImplementedError("creat_table is not implemented, yet")

    def drop_table(self):
        """
            drop the physical table in the DB
        """
        raise NotImplementedError("drop_table is not implemented, yet.")
    
    def upsert(self, many=False):
        """ insert or update intelligently """
        self.last_updated = datetime.datetime.utcnow()
        if self._id == None:
            # insert. so set created at
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.utcnow()
            self.last_updated = self.created_at
        if not many:
            self._id = self.table.insert_one(self.to_dict())
            return self._id
        else:
            raise NotImplementedError("upsert many is not implemented yet")
    
    
    def delete(self, id, session=None):
        """ delete item """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def find_by_id(self, id, use_object_id=False):
        """ return result by id (only)
            parameter:  use_object_id if true find by MongoDB ObjectID
                        else use the PoW id (uuid4)
        """
        if use_object_id:
            return self.table.find_one({"_id": id})
        else:
            return self.table.find_one({"id": id})


    def from_statement(self, statement):
        """ execute a given DB statement raw """
        raise NotImplementedError("from_statement is not available for mongoDB.")

    def page(self, *criterion, limit=None, offset=None):
        """ return the next page of results. See config["myapp"].page_size """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def find(self,*criterion):
        """ Find something given a query or criterion """
        print("Find parameter:" + criterion)
        return self.table.find(criterion)
    
    def find_all(self, *criterion, raw=False, as_json=False, limit=None, offset=None):
        """ Find something given a query or criterion and parameters """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
    def find_one(self, *criterion, as_json=False):
        """ find only one result. Raise Excaption if more than one was found"""
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def find_first(self, *criterion, as_json=False):
        """ return the first hit, or None"""
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def q(self):
        """ return a raw query so the user can do
            everything the DB offers without limitations
        
            for sqlalchemy: return session.query(self.__class__)
            for elastic: return  Q
            for tinyDB return Query
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")
        



