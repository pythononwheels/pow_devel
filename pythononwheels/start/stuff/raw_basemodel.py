
 
from tinydb import TinyDB, Query
from {{appname}}.powlib import pluralize
import datetime
from cerberus import Validator
import xmltodict
import json
import datetime, decimal
from {{appname}}.config import myapp

#print ('importing module %s' % __name__)
class TinyBaseModel():
    

    id =  Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, onupdate=datetime.datetime.now, default=func.now())
    session = session

    
    def init_on_load(self, *args, **kwargs):
 
        self.session=None
        self.tablename = pluralize(self.__class__.__name__.lower())
        
        #
        # if there is a schema (cerberus) set it in the instance
        #
        if "schema" in self.__class__.__dict__:
            print(" .. found a schema for: " +str(self.__class__.__name__) + " in class dict")
            self.schema = self.__class__.__dict__["schema"]            

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
                if key in self.__class__.__dict__:
                    setattr(self, key, kwargs[key])
          
    def api(self):
        """ just for conveniance """
        return self.show_api()

    def show_api(self):
        """
            prints the "external API of the class.
            No under or dunder methods
            And methods only.

            Uses inspect module.
        """
        import inspect
        print(50*"-")
        print("  external API for " + self.__class__.__name__)
        print(50*"-")
        for elem in inspect.getmembers(self, predicate=inspect.ismethod):
            meth = elem[0]

            if not meth.startswith("_"):
                print("  .. " + str(elem[0]) , end="")
                func=getattr(self,elem[0])
                if func:
                    print( str(func.__doc__)[0:100])
                else:
                    print()

    def validate(self):
        """
            checks if the instance has a schema.
            validatees the current values
        """
        if getattr(self,"schema", False):
            # if instance has a schema. (also see init_on_load)
            #v = cerberus.Validator(self.schema)
            v = Validator(self.schema)
            if v.validate(self.dict_dump()):
                return True
            else:
                return v

    def init_from_xml(self, data, root="root"):
        """
            makes a py dict from input xml and
            sets the instance attributes 
            root defines the xml root node
            
        """
        d=xmltodict.parse(data)
        d=d[root]
        for key in d:
            print("key: " + key + " : " + str(d[key]) )
            if isinstance(d[key],dict):
                print(d[key])
                for elem in d[key]:
                    if elem.startswith("#"):
                        if key in self.__class__.__dict__:
                            setattr(self, key, d[key][elem])
            else:
                if key in self.__class__.__dict__:
                    setattr(self, key, d[key])

    def init_from_json(self, data):
        """
            makes a py dict from input json and
            sets the instance attributes 
        """
        d=json.loads(data)
        for key in d:
            if key in self.__class__.__dict__:
                setattr(self, key, d[key])

    def init_from_csv(self, keys, data):
        """
            makes a py dict from input ^csv and
            sets the instance attributes 
            csv has the drawback coompared to json (or xml)
            that the data structure is flat.

            first row must be the "column names"
        """
        #assert len(keys) == len(data), raise AssertionError("keys and data must have the same lenght.")
        if not len(keys) == len(data):
            raise AssertionError("keys and data must have the same lenght.")
        for k,d in zip(keys, data):
            setattr(self, k, d)

    def json_dump(self):
        """ just dump to json """
        return json.dump(self)

    def json_load_from_db(self, data, keep_id=False):
        #TODO:  refresh the object from db and return json
        pass

    def print_schema(self):
        print(50*"-")
        print("Schema for: " + str(self.__class__))
        print("{0:30s} {1:20s}".format("Column", "Type"))
        print(50*"-")
        for col in self.__table__._columns:
            print("{0:30s} {1:20s}".format(str(col), str(col.type)))
            #print(dir(col))

    def dict_dump(self):
        d = {}
        exclude_list=["_jsonify","_sa_instance_state", "session", "schema", "table", "tree_parent_id", "tree_children"]
        if getattr(self, "exclude_list", False):
            exclude_list += self.exclude_list
        for elem in vars(self).keys():
            if not elem in exclude_list:
                d[elem] = vars(self)[elem]
        return d

    def get_relationships(self):
        """ Method not available for TinyDB Models """
        raise RuntimeError("Method not available for TinyDB Models ")

    def get_relations(self):
        """
            returns a list of the relation names
            see: http://stackoverflow.com/questions/21206818/sqlalchemy-flask-get-relationships-from-a-db-model
        """
        raise RuntimeError("Method not available for TinyDB Models ")

    def print_full(self):
        #
        # prints everything including related objects in FULL
        # lenghty but you see everything.
        #
        raise RuntimeError("Method not available for TinyDB Models ")

    def __repr__(self):
        #
        # __repr__ method is what happens when you look at it with the interactive prompt
        # or (unlikely: use the builtin repr() function)
        # usage: at interactive python prompt
        # p=Post()
        # p
        from pprint import pformat
        d = self.json_dump()
        return pformat(d,indent=+4)

    def __str__(self):
        #
        # The __str__ method is what happens when you print the object
        # usage:
        # p=Post()
        # print(p)
        return self.__repr__()
                       
    def create_table(self):
        """
            created the physical table in the DB
        """
        pass

    def drop_table(self):
        """
            created the physical table in the DB
        """
        pass
    
    def upsert(self, session=None):
        """ insert oro update intelligently """
        pass     

    def get(self, id):
        """ return by id """
        pass

    def from_statement(self, statement):
        """ Method not available for TinyDB Models """
        raise RuntimeError("Method not available for TinyDB Models ")

    def page(self, *criterion, limit=None, offset=None):
        """ return the next page """
        pass

    def find(self,*criterion):
        """ Find something given a query or criterion """
        pass
    
    def find_all(self, *criterion, raw=False, as_json=False, limit=None, offset=None):
        """ Find something given a query or criterion and parameters """
        pass
    
    def find_one(self, *criterion, as_json=False):
        """ find only one result. Raise Excaption if more than one was found"""
        pass

    def find_first(self, *criterion, as_json=False):
        """ return the first hit, or None"""
        pass

    def q(self):
        """ return a raw query """
        # for sqlalchemy: return session.query(self.__class__)
        # for elastic: return  Q
        # for tinyDB return Query
        pass
        



