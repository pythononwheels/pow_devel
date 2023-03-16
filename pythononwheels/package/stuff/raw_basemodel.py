from {{appname}}.lib.powlib import pluralize
import datetime
import xmltodict
import simplejson as json
import datetime, decimal
from {{appname}}.conf.config import myapp
from {{appname}}.lib.powlib import merge_two_dicts
from {{appname}}.lib.encoders import pow_json_serializer
from {{appname}}.models.modelobject import ModelObject

class <DBNAME>BaseModel(ModelObject):
    """
        The Raw BaseModel Class
    """    

    basic_schema = {
        "id"    :   { "type" : "string" },
        "created_at"    : { "type" : "datetime" },
        "last_updated"    : { "type" : "datetime" },
    }

    def __init__(self, *args, **kwargs):
        """
            
        """
        self.tablename = pluralize(self.__class__.__name__.lower())
        self.index = self.tablename
        super().init_on_load(*args, **kwargs)
    
                           
    #
    # These Mehtods should be implemented by every subclass
    # 
    def to_json(self, *args, **kwargs):
        """ just dump to json formatted string"""
        #return json.dumps(self.db_dict_dump(), *args, default=pow_json_serializer, **kwargs)
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def json_result_to_object(self, res):
        """ returns a list of objects from a given json list (string) """
        #return json.loads(self.json_dumps(*args, **kwargs))
        raise NotImplementedError("Subclasses should overwrite this Method.")

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
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def drop_table(self):
        """
            drop the physical table in the DB
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
    def upsert(self, session=None):
        """ insert or update intelligently """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
    def delete(self, id, session=None):
        """ delete item """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def find_by_id(self, id):
        """ return result by id (only)"""
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def from_statement(self, statement):
        """ execute a given DB statement raw """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def page(self, *criterion, limit=None, offset=None):
        """ return the next page of results. See config["myapp"].page_size """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def find(self,*criterion):
        """ Find something given a query or criterion """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
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
        



