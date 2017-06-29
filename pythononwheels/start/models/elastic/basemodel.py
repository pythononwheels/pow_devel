from {{appname}}.powlib import pluralize
import datetime
import xmltodict
import simplejson as json
import datetime, decimal
from {{appname}}.config import myapp
from {{appname}}.powlib import merge_two_dicts
from {{appname}}.encoders import pow_json_serializer
from {{appname}}.models.modelobject import ModelObject
from {{appname}}.powlib import merge_two_dicts
from {{appname}}.database.elasticdblib import es,dbname

class ElasticBaseModel(ModelObject):
    """
        The ElasticSearch BaseModel Class
    """    

    basic_schema = {
        "created_at"    : { "type" : "datetime" },
        "last_updated"    : { "type" : "datetime" },
    }


    def __init__(self, *args, **kwargs):
        """
            constructor
        """
        #super(ModelObject, self).init_on_load(*args, **kwargs)
        self.tablename = pluralize(self.__class__.__name__.lower())
        self.doc_type = self.tablename
        self.dbname = dbname
        
        #
        # if there is a schema (cerberus) set it in the instance
        #
        if "schema" in self.__class__.__dict__:
            print(" .. found a schema for: " +str(self.__class__.__name__) + " in class dict")
            self.schema = merge_two_dicts(
                self.__class__.__dict__["schema"],
                self.__class__.basic_schema)
            print("  .. Schema is now: " + str(self.schema))
        

    #
    # These Methods should be implemented by every subclass
    # 
        
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
    
    def create(self):
        """ first time sabve an instance to DB """
        self.last_updated = datetime.datetime.now()
        self.created = self.last_updated
        res = es.index(index=dbname, doc_type=self.doc_type, body=self.to_json())

    def upsert(self, session=None):
        """ insert or update intelligently """
        self.last_updated = datetime.datetime.now()
        res = es.index(index=dbname, doc_type=self.doc_type, body=self.to_json())

        if res.get("_id",None):
            self._id = res.get("_id")
        return res

    def find_by_id(self, id=None):
        """ return result by id (only)"""
        if id:
            es.get(index=dbname, doc_type=self.doc_type, id=id)
        else:
            es.get(index=dbname, doc_type=self.doc_type, id=self._id)
        

    def from_statement(self, statement):
        """ execute a given DB statement raw """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def page(self, *criterion, limit=None, offset=None):
        """ return the next page of results. See config["myapp"].page_size """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def find(self,body):
        """ Find something given a query or criterion """
        res = es.search(index=dbname, body=body)
        return res
    
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
        



