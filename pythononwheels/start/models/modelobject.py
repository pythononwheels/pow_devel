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
from {{appname}}.decoders import pow_init_from_dict_deserializer

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
    
    # def setup_dirty_model(self):
    #     """
    #         Tracks changes in the instance relative to last save to DB
    #         Rails: see: https://apidock.com/rails/ActiveRecord/Dirty
    #     """
    #     # will hold last value before change + a flag if this attribute is dirty.
    #     self.dirty = {}
    #     self.is_dirty = False

    # def rollback_dirty(self, name=None):
    #     """
    #         Rolls back the changes made to the object since last save operation to DB
    #         see: https://apidock.com/rails/ActiveRecord/Dirty
    #         This is NOT a DB rollback.
    #         Look at session.rollback() Bfor SQL or accordinug for mongoDB > 4 or other transation capable DBs
    #     """
    #     if self.is_dirty:
    #         if name in self.dirty:
    #             # only rollback attribute changes for name
    #             try:
    #                 setattr(self, name, self.dirty[name]["value"])
    #                 self.dirty.pop(name, None)
    #                 # check if still elements in dirty
    #                 if not self.dirty:
    #                     self.is_dirty = False
    #             except Exception as e:
    #                 print("ERROR Dirty rollback : {}".format(str(e)))
    #         # else: rollback all changes
    #         for elem in self.dirty:
    #             try:
    #                 setattr(self, elem, self.dirty[elem]["value"])
    #             except Exception as e:
    #                 print("ERROR Dirty rollback : {}".format(str(e)))
    
    # def was(self,name):
    #     """
    #         returns the value that attribute name had before the last save to DB operation (dirty object)
    #         see: https://apidock.com/rails/ActiveRecord/Dirty
    #     """
    #     try:
    #         return self.dirty[name]["value"]
    #     except Exception as e:
    #         raise e
    
    # def changed(self,name):
    #     """
    #         returns the value and changed value that attribute name had before the last save to 
    #         DB operation (dirty object)
    #         see: https://apidock.com/rails/ActiveRecord/Dirty
    #     """
    #     try:
    #         return [self.dirty[name]["value"], getattr(self,name)]
    #     except Exception as e:
    #         raise e

    def __setattr__(self, name, value):
        #print("trying to set attribute: {} -> to {}".format(str(name), str(value)))
        #
        # try to convert the value to the schema type
        #
        d={}
        d[name]=value
        d=pow_init_from_dict_deserializer(d, self.schema, simple_conversion=myapp["simple_conversion"])
        # check if dirty mark has to be set.
        # if name in self.schema:
        #     try:
        #         current_value = getattr(self, name)
        #         if value != current_value and not name in self.dirty:
        #             #has changed, so save the old val and mark as dirty:
        #             self.dirty[name] =  { "value" : current_value, "dirty" : True }
        #             self.is_dirty = True
        #     except:
        #         pass
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
                    print(str(e))
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
            self.__class__.observers_initialized = True
            #print (" ... Found None: {}".format(str(e) ))
          
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
        try:
            d=pow_init_from_dict_deserializer(d,self.schema, simple_conversion)
        except:
            raise
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
    
    
    def init_from_json_file(self, json_file=None, ignore=True, simple_conversion=False):
        """
            returns a generator that yields models instances per row
            of the json file.
            ignore = True => set the attribute even if it is not in the schema
            simple_conversion => try to convert the values to their schema definitions.
        """
        with open(json_file) as f:
            data = json.load(f)
            for d in data:
                m = self.__class__()
                try:
                    m.init_from_dict(d, ignore, simple_conversion=simple_conversion)
                    yield m
                except:
                    raise
                


    def init_from_json(self, data, ignore=True, simple_conversion=False):
        """
            makes a py dict from input json and
            sets the instance attributes 
            sets the attributes on self if len(data) == 1
            returns a generator if len(data)>1
        """
        if isinstance(data, bytes):
            data=data.decode(myapp["byte_decoding"])
        d=json.loads(data,object_hook=pow_json_deserializer)
        return self.init_from_dict(d, ignore, simple_conversion=simple_conversion)
        #else:
        #    for d in data:
        #        m = self.__class__()
        #        m.init_from_dict(d, ignore, simple_conversion=simple_conversion)
        #        yield m
    
    # def init_from_json(self, data, ignore=True, simple_conversion=False):
    #     """
    #         makes a py dict from input json and
    #         sets the instance attributes 
    #     """
    #     d=json.loads(data,object_hook=pow_json_deserializer)
    #     return self.init_from_dict(d, ignore, simple_conversion=simple_conversion)

    def init_from_csv_file(self, csv_file=None, newline='', ignore=True):
        """
            inits instances of this model from the given csv
            returns a generator that yields models instances per row
            of the csv file.
        """
        import csv
        with open(csv_file, newline=newline) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print(row)
                m = self.__class__()
                for key,value in row.items():
                    if ignore:
                        setattr(m, key, value)
                    else:
                        if key in self.schema:
                            setattr(m, key, value)
                        else:
                            raise Exception(" Key: " + str(key) + " is not in schema for: " + self.__class__.__name__)
                yield m
        
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
    
    def to_xml(self):
        """
            returns an xml representation of the model
            using the configured xml encoder from config->my_app->encoders->xml
        """
        try:
            encoder = myapp["encoder"]["xml"]
            return encoder.dumps(self.to_dict(), root=self.__class__.__name__)
        except:
            raise Exception("ERROR: problems to convert to xml. Probably no encoder defined in config.")
    
    
    def to_json_file(self, data=[], filename=None):
        """
            if data==[] just save this model to json
            else create a json file with the givel list of models.
        """
        if not filename:
            filename=self.__class__.__name.__ + "_" + datetime.datetime.utcnow().isoformat() + ".json"
        with open(filename, "w") as outfile:
            if len(data)==0:
                # just me
                outfile.write(self.to_json())
            else:
                outfile.write("[")
                counter = 0
                length = len(data)
                for elem in data:
                    counter += 1
                    if counter < length:
                        outfile.write(elem.to_json() + "," + "\\n" )
                    else:
                        outfile.write(elem.to_json() ) 
                outfile.write("]")
        print(" ..JSON written to: {}".format(filename))
    
    def res_to_json(self, res):
        """
            returns a list of results in a json serialized format.
        """
        if not isinstance(res, list):
            try:
                res = list(res)
            except:
                return res.to_json()
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
            
    def to_csv_file(self, data=[], filename=None):
        """
            if data==[] just save this model to json
            else create a json file with the givel list of models.
        """
        import csv
        if not filename:
            filename=self.__class__.__name__ + "_" + datetime.datetime.utcnow().isoformat() + ".csv"
        
        with open(filename, "w") as outf:
            # write the header
            #outfile.write(",".join([str(x) for x in self.schema.keys()]) +"\\n")
            writer = csv.DictWriter(outf, self.schema.keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row.to_dict())
        
        print(" ..CSV written to: {}".format(filename))
    
    def to_dict(self, lazy=True):
        """
            return vars / attributes of this instance as dict
            raw = True => all (almost: except for those in exclude_list)
            raw = False => only those defined in schema
        """
        d = {}
        # return just the attributes that are defined in the schema 
        # + those define in include_attrs model class variable.
        include_attrs = getattr(self, "include_attributes", [])
        for elem in list(self.schema.keys()) + include_attrs:
            val = getattr(self,elem, None)
            if lazy:
                d[elem] = val
            else:
                if val:
                    d[elem] = val
        return d
    
    def res_to_dict(self, res):
        """
            returns a list of results in a list of dicts.
        """
        if not isinstance(res, list):
            try:
                res = list(res)
            except:
                return res.to_dict()
          
        reslist =  [x.to_dict() for x in res]
        if len(reslist) == 1:
            return reslist[0]
        else:
            return reslist


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
        



