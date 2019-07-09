from {{appname}}.database.mongodblib import db, client
from {{appname}}.powlib import pluralize
import datetime
import xmltodict
import simplejson as json
import datetime, decimal
from {{appname}}.config import myapp
from {{appname}}.powlib import merge_two_dicts
from {{appname}}.encoders import pow_json_serializer
from {{appname}}.models.modelobject import ModelObject
from bson.json_util import dumps

import pymongo
import uuid

class MongoBaseModel(ModelObject):
    """
        The Raw BaseModel Class
    """    

    basic_schema = {
        "id"    :   { "type" : "string", "default" : None },
        "_uuid"    :   { "type" : "string", "default" : None },
        "created_at"    : { "type" : "datetime", "default" : None },
        "last_updated"    : { "type" : "datetime", "default" : None },
    }

    def init_on_load(self, *args, **kwargs):
        """
            basic setup for all mongoDB models.
        """
        #print("executin init_on_load")
        
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
        #for key in self.schema.keys():
        #    if self.schema[key].get("default", None) != None:
        #        setattr(self,key,self.schema[key].get("default"))
        #        self.schema[key].pop("default", None)
        #    else:
        #        #print("no default for: " + str(self.schema[key]))
        #        setattr(self, key, None)
        self.setup_instance_values()           
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
        
        self.table = db[pluralize(self.__class__.__name__.lower())]
        self.collection = self.table
        self.table.create_index([('id', pymongo.ASCENDING)], unique=True)
        
        self.tablename = pluralize(self.__class__.__name__.lower())
        #self.table = self.__class__.table
        self._id = None
        self.id = str(uuid.uuid4())
        self._uuid = self.id
        #print("new id is: " + self.id) 
        self.init_observers()
        #self.setup_dirty_model()
                           
    #
    # These Methods should be implemented by every subclass
    # 
    def get(self, name):
        return getattr(self,name)
    
    def to_json(self):
        """ just dump to json formatted string
            parameter:  res must be pymongo cursor. 
                        Example: res = self.table.find() 
        """
        # uses bson.json_util dumps
        from bson.json_util import DEFAULT_JSON_OPTIONS
        DEFAULT_JSON_OPTIONS.datetime_representation = 2
        return dumps(self.to_dict())

    # def init_from_json(self, data, ignore=False):
    #     """
    #         makes a py dict from input json and
    #         sets the instance attributes 
    #     """
    #     from bson.json_util import loads
    #     print(data)
    #     try:
    #         d=loads(data)
    #     except Exception as e:
    #         print("Ex1 : " + str(e))
    #         try:
    #             d=loads(data.decode("utf-8") )
    #         except Exception as e:
    #             print("E2: " + str(e))
    #             raise e
    #     print(d)
    #     print(str(type(d)))
    #     return self.init_from_dict(d, ignore)


    def json_result_to_object(self, res):
        """
            returns a list of objects from a given json list (string) 
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
    def _get_next_object(self, cursor):
        """
            return a generator that creates a Model object
            for each next call.
        """
        for elem in cursor:
            m=self.__class__()
            m.init_from_dict(elem)
            yield m
    

    def _return_find(self, res):
        """ 
            returns a list of models from a given cursor.
            parameter:  res can be pymongo cursor or is handled as a single document (dict). 
                        Example: res = self.table.find() 
            returns: a sinlge Model or a [Models]
        """ 
        # single result element
        if not isinstance(res, (pymongo.cursor.Cursor)):       
            m=self.__class__()
            m.init_from_dict(res)
            #print("returning: " +str(m))
            #print("   type: " + str(type(m)))
            return m
        
        # return the generator function. 
        return self._get_next_object(res)
        # handle cursor (many result elelemts)
        # reslist = []
        # for elem in res:
        #     m=self.__class__()
        #     m.init_from_dict(elem)
        #     #print("appending: " +str(m))
        #     #print("   type: " + str(type(m)))
        #     reslist.append(m)
        # return reslist

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
    

    def upsert(self):
        """ insert or update intelligently """
        #self.last_updated = datetime.datetime.utcnow().strftime(myapp["datetime_format"])
        if self.observers_initialized:
            for observer in self.observers:
                try:
                    observer.before_upsert(self)
                except:
                    pass
        self.last_updated = datetime.datetime.utcnow()
        if self.observers_initialized:
                for observer in self.observers:
                    try:
                        ret = observer.before_upsert(self)
                    except:
                        pass
        if self._id == None:
            #print("** insert **")
            # insert. so set created at            
            self.created_at = datetime.datetime.utcnow().strftime(myapp["datetime_format"])
            self.last_updated = self.created_at
            ior = self.table.insert_one(self.to_dict())
            self._id = ior.inserted_id
            return self._id
        else:
            # update
            #print("** update **")
            #print(self.to_dict())
            self.last_updated = datetime.datetime.utcnow().strftime(myapp["datetime_format"])
            ior = self.table.update_one({"_id" : self._id}, {"$set": self.to_dict()}, upsert=False )
            return ior
        # clean dirty marks
        self.dirty = {}
        self.is_dirty = False
       
    def delete(self, filter=None, many=False):
        """ delete item """
        if filter == None:
            filter = {"id" : self.id }
        # clean dirty marks
        self.dirty = {}
        self.is_dirty = False
        if not many:
            return self.table.delete_one(filter)
        else:
            return self.table.delete_many(filter)


    def find_by_id(self, id, use_object_id=False):
        """ return result by id (only)
            parameter:  use_object_id if true find by MongoDB ObjectID
                        else use the PoW id (uuid4)
        """
        if use_object_id:
            return self.find_one({"_id": id})
        else:
            return self.find_one({"id": id})


    def from_statement(self, statement):
        """ execute a given DB statement raw """
        raise NotImplementedError("from_statement is not available for mongoDB.")

    def page(self, filter={}, page=0, page_size=None):
        """ return the next page of results. See config["myapp"].page_size 
            actually means: (taking the sql understandng)
                 page === offset 
                 limit === limit
        """
        if page_size == None:
            page_size = myapp["page_size"] 
        return self._return_find(self.table.find(filter).skip(page*page_size).limit(page_size))

    def find(self,filter={}, raw=False):
        """ Find something given a query or criterion 
            filter = { "key" : value, ..}
        """
        #print("Find parameter:" + str(filter))
        if raw:
            return self.table.find(filter)
        return self._return_find(self.table.find(filter))
    
    def find_all(self, filter=None, raw=False, limit=0, offset=0):
        """ Find something given a query or criterion and parameters """
        if (limit>0) or (offset>0):
            return self.page(filter=filter, limit=limit, offset=offset)
        else:
            return self.find(filter)
    
    def get_all(self):
        """ just a synonym for find_all . but without any filters or limits. """
        return self.find_all()

    def find_one(self, filter={}):
        """ find only one result. Raise Excaption if more than one was found"""
        res = self.table.find_one(filter)
        if res != None:
            return self._return_find(res)
        else:
            return None
        
    def find_first(self, filter={}):
        """ return the first hit, or None"""
        raise NotImplementedError("Not available for MongoDB")

    def q(self):
        """ return a raw query so the user can do
            everything the DB offers without limitations
        
            for sqlalchemy: return session.query(self.__class__)
            for elastic: return  Q
            for tinyDB return Query
            for MongoDB: not implemented
        """
        return self.table
        



