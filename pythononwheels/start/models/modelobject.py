from {{appname}}.powlib import pluralize
import datetime
from cerberus import Validator
import xmltodict
import simplejson as json
import datetime, decimal
from {{appname}}.config import myapp
from {{appname}}.powlib import merge_two_dicts
from {{appname}}.encoders import pow_json_serializer
from {{appname}}.decoders import pow_json_deserializer
import {{appname}}.config as cfg
from insight_dash.decoders import pow_init_from_dict_deserializer

class ModelObject():
    """
        The BaseClass for all PoW Model Classes
    """    
    # if you need a basic schema in the class override this (see tinyDB BaseModel)
    basic_schema={}
    observers_initialized = False
    observers = []
    autocommit = True
    

    def init_on_load(self, *args, **kwargs):
        """
            should be called from instances or BaseModels __init__
            will be called by sqlalchemy automatically on model creation
        """
        self.tablename = pluralize(self.__class__.__name__.lower())
        
        self.setup_instance_schema()        
        
        if "format" in kwargs:
            self.setup_from_format( args, kwargs)
    
    def setup_dirty_model(self):
        """
            Tracks changes in the instance relative to last save to DB
            Rails: see: https://apidock.com/rails/ActiveRecord/Dirty
        """
        # will hold last value before change + a flag if this attribute is dirty.
        self.dirty = {}
        self.is_dirty = False

    def rollback_dirty(self, name=None):
        """
            Rolls back the changes made to the object since last save operation to DB
            see: https://apidock.com/rails/ActiveRecord/Dirty
            This is NOT a DB rollback.
            Look at session.rollback() Bfor SQL or accordinug for mongoDB > 4 or other transation capable DBs
        """
        if self.is_dirty:
            if name:
                # only rollback attribute changes for name
                try:
                    setattr(self, name, self.dirty[name]["value"])
                except Exception as e:
                    print("ERROR Dirty rollback : {}".format(str(e)))
            # else: rollback all changes
            for elem in self.dirty:
                try:
                    setattr(self, elem, self.dirty[elem]["value"])
                except Exception as e:
                    print("ERROR Dirty rollback : {}".format(str(e)))
    
    def was(self,name):
        """
            returns the value that attribute name had before the last save to DB operation (dirty object)
            see: https://apidock.com/rails/ActiveRecord/Dirty
        """
        try:
            return self.dirty[name]["value"]
        except Exception as e:
            raise e
    
    def changed(self,name):
        """
            returns the value and changed value that attribute name had before the last save to 
            DB operation (dirty object)
            see: https://apidock.com/rails/ActiveRecord/Dirty
        """
        try:
            return [self.dirty[name]["value"], getattr(self,name)]
        except Exception as e:
            raise e

    def __setattr__(self, name, value):
        #print("trying to set attribute: {} -> to {}".format(str(name), str(value)))
        #
        # try to convert the value to the schema type
        #
        d={}
        d[name]=value
        d=pow_init_from_dict_deserializer(d, self.schema, simple_conversion=myapp["simple_conversion"])
        # check if dirty mark has to be set.
        if name in self.schema:
            try:
                current_value = getattr(self, name)
                if value != current_value and not name in self.dirty:
                    #has changed, so save the old val and mark as dirty:
                    self.dirty[name] =  { "value" : current_value, "dirty" : True }
                    self.is_dirty = True
            except:
                pass
        # set the value
        super().__setattr__(name, d[name])
    
    #
    # These Methods can normally be inherited
    # 
    def setup_instance_schema(self):
        """
            if there is a schema (cerberus) set it in the instance
        """
        if "schema" in self.__class__.__dict__:
            print(" .. found a schema for: " +str(self.__class__.__name__) + " in class dict")
            self.schema = merge_two_dicts(
                self.__class__.__dict__["schema"],
                basic_schema)
        print("  .. Schema is now: " + str(self.schema))

    def setup_instance_values(self):
        """ fills the instance with defined default values"""
        for key in self.schema.keys():
            if self.schema[key].get("default", None) != None:
                setattr(self,key,self.schema[key].get("default"))
                self.schema[key].pop("default", None)
            else:
                #print("no default for: " + str(self.schema[key]))
                #print("trying: " + str(cfg.database["default_values"][self.schema[key]["type"]]))
                try:
                    #print("trying: " + config.database["default_values"][self.schema[key]["type"]])
                    setattr(self,key,cfg.database["default_values"][self.schema[key]["type"]])
                except Exception as e:
                    print(e.message)
                    setattr(self, key, None)
        
    def setup_from_format(self, *args, **kwargs):
        """
            setup values from kwargs or from init_from_<format> if format="someformat"
            example: m = Model( data = { 'test' : 1 }, format="json")
            will call m.init_from_json(data)
        """
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
                if key in self.schema:
                    setattr(self, key, kwargs[key])

    def init_observers(self):
        #
        # Try to find Observers.
        # 
        if self.__class__.observers_initialized:
            return
        obs = getattr(self,"observers", False)
        if obs:
            # try to load the classes and fire their action on the corresponding model actions.
            # rails:  (remark: obervers are a separate module since 3.2)
            #   https://api.rubyonrails.org/v3.2.13/classes/ActiveRecord/Callbacks.html
            #   https://api.rubyonrails.org/v3.2.13/classes/ActiveRecord/Observer.html#method-i-define_callbacks
            # pow:
            #   before & after:  save, create, commit, validation, delete.
            pass
        from pydoc import locate
        print("trying to find possible observer in {}".format(
            str(self.__class__.__module__)+"_observer."+ str(self.__class__.__name__)+ "Observer"
            )
        )
        try:
            obs = locate(str(self.__class__.__module__) +"_observer." +  str(self.__class__.__name__) + "Observer")
            o=obs()
            print(" ... Found: {}".format(str(o.__class__)))
            self.__class__.observers_initialized = True
            self.__class__.observers.append(o)
        except Exception as e:
            print (" ... Found None: {}".format(str(e) ))
          
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
                print("{0:30s}".format("  .. " +str.strip(meth)), end="")
                #  print("  method:  " + str.strip(meth) , end="")
                func=getattr(self,meth)
                if func:
                    if func.__doc__:
                        print( "  -->  " + str.strip(func.__doc__[0:50]))
                    else:
                        #print( "             No docstring  ")
                        print()
                else:
                    print()

    def validate(self):
        """
            checks the instance against a schema.
            validatees the current values
        """            
        if getattr(self,"schema", False):
            # if instance has a schema. (also see init_on_load)
            #v = cerberus.Validator(self.schema)
            v = Validator(self.schema)

            if self.observers_initialized:
                for observer in self.observers:
                    try:
                        ret = observer.before_validate(self, v)
                    except:
                        pass
            
            res = v.validate(self.to_dict(lazy=False))
            if self.observers_initialized:
                for observer in self.observers:
                    try:
                        ret = observer.after_validate(self, res)
                    except:
                        pass
            if v.validate(self.to_dict(lazy=False)):
                return (True, None)
            else:
                return (False,v)
    
    def init_from_dict(self, d, ignore=True, simple_conversion=False):
        """
            creates a Model from the given data dictionary
            simple_conversion = True tries to use simple logic to create 
                a little bit more advanced python data types.
                for example "a b c" will be model.attribute = "a b c".split(myapp["list_separator"])
                Mainly used for handling request from simple html form scaffolding 
        """
        from {{appname}}.decoders import pow_init_from_dict_deserializer
        #print("init from dict")
        #print(d)
        d=pow_init_from_dict_deserializer(d,self.schema, simple_conversion)
        #print("after conversion: ")
        #for elem in d:
        #    print(str(elem) + "->" + str(type(elem)))
        for key in d:
            if ignore:
                setattr(self, key, d[key])
            else:
                if key in self.schema:
                    setattr(self, key, d[key])
                else:
                    raise Exception(" Key: " + str(key) + " is not in schema for: " + self.__class__.__name__)
        

    def init_from_xml(self, data, root="root", ignore=True):
        """
            makes a py dict from input xml and
            sets the instance attributes 
            root defines the xml root node
            
        """
        d=xmltodict.parse(data)
        d=d[root]
        for key in d:
            #print("key: " + key + " : " + str(d[key]) )
            if isinstance(d[key],dict):
                print(d[key])
                for elem in d[key]:
                    if elem.startswith("#"):
                        if key in self.__class__.__dict__:
                            setattr(self, key, d[key][elem])
            else:
                #if key in self.__class__.__dict__:
                if ignore:
                    setattr(self, key, d[key])
                else:
                    if key in self.schema:
                        setattr(self, key, d[key])
                    else:
                        raise Exception(" Key: " + str(key) + " is not in schema for: " + self.__class__.__name__)

    def init_from_json(self, data, ignore=False, simple_conversion=False):
        """
            makes a py dict from input json and
            sets the instance attributes 
        """
        d=json.loads(data,object_hook=pow_json_deserializer)
        return self.init_from_dict(d, ignore, simple_conversion=simple_conversion)


    def init_from_csv(self, keys, data, ignore=True):
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
            if ignore:
                setattr(self, k, d)
            else:
                if key in self.schema:
                    setattr(self, key, d[key])
                else:
                    raise Exception(" Key: " + str(key) + " is not in schema for: " + self.__class__.__name__)
    
    def to_json(self, *args, default=pow_json_serializer, **kwargs):
        """ just json """
        #return json.loads(self.json_dumps(*args, **kwargs))
        return json.dumps(self.to_dict(), *args, default=default, **kwargs)
    
    
    def res_to_json(self, res):
        """
            returns a list of results in a json serialized format.
        """
        if not isinstance(res, type([])):
            res = [res]
        #return json.loads(json.dumps(res, default=pow_json_serializer))   
        reslist =  [x.to_json() for x in res]
        if len(reslist) == 1:
            return reslist[0]
        else:
            return reslist
         
    def to_csv(self, encoder=None):
        """ returns the models as csv using the given encoder.
            if no encoder is given the defined encoders from config.py are taken.
        """
        if encoder:
            encoder = encoder
        else:
            encoder = myapp["encoder"]["csv"]
        return encoder.dumps(self.to_json())
            

    def to_dict(self, lazy=True):
        """
            return vars / attributes of this instance as dict
            raw = True => all (almost: except for those in exclude_list)
            raw = False => only those defined in schema
        """
        d = {}
        # return just the attributes that are defined in the schema 
        for elem in self.schema.keys():
            val = getattr(self,elem, None)
            if lazy:
                d[elem] = val
            else:
                if val:
                    d[elem] = val
        return d
        


    def print_full(self):
        """ Subclasses should overwrite this Method. 
            prints every attribute including related objects in FULL
            lenghty but you see everything.
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def __repr__(self):
        """
            __repr__ method is what happens when you look at it with the interactive prompt
            or (unlikely: use the builtin repr() function)
            usage: at interactive python prompt
            p=Post()
            p
        """
        from pprint import pformat
        #j = self.json_dump()
        j = self.to_dict()
        return pformat(j,indent=+4)

    def __str__(self):
        """
            The __str__ method is what happens when you print the object
            usage:
            p=Post()
            print(p)
        """
        return self.__repr__()
    
    def get(self, name)                       :
        """
            returns the attribute with the given name 
        """
        return getattr(self, name, None)
    #
    # These Mehtods should be implemented by every subclass
    # 
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
        



