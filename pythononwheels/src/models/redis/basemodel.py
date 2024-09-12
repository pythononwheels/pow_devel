from {{appname}}.database.redisdblib import redisdb 
from {{appname}}.models.modelobject import ModelObject
from {{appname}}.lib.powlib import merge_two_dicts
import uuid

class RedisBaseModel(ModelObject):
    """
        The PoW Basemode for RedisDB
        Keep this as simple as possible
    """
    
   

    # set the db
    db=redisdb

    def init_on_load(self, *args, **kwargs):
        """
            make the neccessary basic inits
        """
        self.basic_schema = {
            "_uuid" :  { "type" : "string", "default" : str(uuid.uuid4()) },
            #"eid"   :   { "type" : "string" },
            "created_at"    : { "type" : "datetime" },
            "last_updated"    : { "type" : "datetime" },
        }
        
        self.setup_instance_schema()
        self.setup_instance_values()
        self.setup_from_format(**kwargs)
        self.setup_from_kwargs(**kwargs)
        self.init_observers()
        self.key=None 

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
            created the physical table in the DB
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def drop_table(self):
        """
            created the physical table in the DB
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
    def upsert(self, session=None):
        """ insert oro update intelligently """
        if self.key != None:
            self.db.set(self.key, self.to_json())
        else:
            raise Exception("Error: no key set!")
    
    
    def find_by_id(self, id=None):
        """ return result by id (only)"""
        if id != None:
            return self.db.get(id)
        else:
            # take this instance's key
            if self.key != None:
                return self.db.get(self.key)
            else:
                raise Exception("Error: no key set!")
    
    def get_keys(self):
        """
            careful: runs O(n) for large datasets maybe very slow
        """
        return self.db.keys()
        

    def from_statement(self, statement):
        """ execute a given DB statement raw """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def page(self, *criterion, limit=None, offset=None):
        """ return the next page of results. See config["myapp"].page_size """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def find(self, id=None):
        """ Find something given a query or criterion """
        return self.find_by_id(id)
    
    def find_all(self, *criterion, raw=False, limit=None, offset=None):
        """ Find something given a query or criterion and parameters """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
    def find_one(self, *criterion):
        """ find only one result. Raise Excaption if more than one was found"""
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def find_first(self, *criterion):
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