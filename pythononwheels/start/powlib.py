import re
import os

from sqlalchemy import Table
import logging
import copy
from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from sqlalchemy import Unicode, Text, Boolean, Numeric, BigInteger, LargeBinary
import werkzeug.security
from {{appname}}.config import myapp 
from sqlalchemy.ext.declarative.api import DeclarativeMeta

class PowBaseMeta(DeclarativeMeta):
    """
        Base Metaclass for PoW SQL Models.
        Main purpose is to add or remove the default attirbutes on class level        
        (toggle with _use_pow_schema_attrs = Fasle | True in the model)
    """
    def __init__(cls, name, bases, dct):
        print("cls: {}, name: {}".format(str(cls), str(name)))
        print(cls.__dict__.keys())
        # if '_use_pow_schema_attrs' not in cls.__dict__:
        #     print("has _use_pow_schema_attrs = No")
        # else:
        #     print("has _use_pow_schema_attrs = Yes")
        from sqlalchemy.sql.expression import func 
        if hasattr(cls, '_use_pow_schema_attrs'):
            if getattr(cls,'_use_pow_schema_attrs'):
                setattr(cls,"id", Column(Integer, primary_key=True))
                setattr(cls,"created_at",Column(DateTime, default=func.now()))
                setattr(cls, "last_updated", Column(DateTime, onupdate=func.now(), default=func.now()))
            else:
                print("not adding pow schema attrs")
        else:
            setattr(cls,"id", Column(Integer, primary_key=True))
            setattr(cls,"created_at",Column(DateTime, default=func.now()))
            setattr(cls, "last_updated", Column(DateTime, onupdate=func.now(), default=func.now()))
        super().__init__(name, bases, dct)

def check_password_hash(pwhash, password ):
    """
        uses werkzeug.security.check_password_hash
        see: http://werkzeug.pocoo.org/docs/0.14/utils/#module-werkzeug.security
        get the password from for example a login form (make sure you use https)
        get the hash from the user model table (see generate_password_hash below)
    """
    return werkzeug.security.check_password_hash(pwhash, password)

def generate_password_hash( password ):
    """
        uses werkzeug.security.generate_password_hash 
        see: http://werkzeug.pocoo.org/docs/0.14/utils/#module-werkzeug.security
        store this returned hash in the user models table as password
        when the user is first registered or changed his password.
        Use https to secure the plaintext POSTed pwd.
    """
    method = myapp["pwhash_method"]
    return werkzeug.security.generate_password_hash(password, method=method, salt_length=8)

def make_logger(name, level, handler, format=None, logfile=None):
    """
        get the given logger and configure it 
        with handler, and format

        loglevels:
        ------------------------------
        Level       Numeric value
        CRITICAL        50
        ERROR           40
        WARNING         30
        INFO            20
        DEBUG           10
        NOTSET           0
    """
    log_file_name = logfile
    handler_log_level = logging.INFO
    logger_log_level = logging.DEBUG

    db_handler = logging.FileHandler(db_log_file_name)
    db_handler.setLevel(db_handler_log_level)

    db_logger = logging.getLogger('sqlalchemy')
    db_logger.addHandler(db_handler)
    db_logger.setLevel(db_logger_log_level)
    return logger

def get_class_name(name):
    """
        tries to return a CamelCased class name as good as poosible
        capitalize
        split at underscores "_" and capitelize the following letter
        merge
        this_is_Test => ThisIsTest
        test => Test
        testone => Testone
    """
    #print("class_name: " + "".join([c.capitalize() for c in name.split("_")]))
    return "".join([c.capitalize() for c in name.split("_")])


#see: http://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
# but I need a deep copy here. 
def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = copy.deepcopy(x)
    #z = x.copy()
    z.update(y)
    return z

# (pattern, search, replace) regex english plural rules tuple
# taken from : http://www.daniweb.com/software-development/python/threads/70647
rule_tuple = (
    ('[ml]ouse$', '([ml])ouse$', 'ice'),
    ('child$', 'child$', 'children'),
    ('booth$', 'booth$', 'booths'),
    ('foot$', 'foot$', 'feet'),
    ('ooth$', 'ooth$', 'eeth'),
    ('l[eo]af$', 'l([eo])af$', 'laves'),
    ('sis$', 'sis$', 'ses'),
    ('man$', 'man$', 'men'),
    ('ife$', 'ife$', 'ives'),
    ('eau$', 'eau$', 'eaux'),
    ('lf$', 'lf$', 'lves'),
    ('ees$', 'ees$', 'es'),
    ('[sxz]$', '$', 'es'),
    ('[^aeioudgkprt]h$', '$', 'ees'),
    ('(qu|[^aeiou])y$', 'y$', 'ies'),
    ('$', '$', 's')
    )
def regex_rules(rules=rule_tuple):
    # also to pluralize
    for line in rules:
        pattern, search, replace = line
        yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)

def plural(noun):
    #print noun
    # the final pluralisation method.
    for rule in regex_rules():
        result = rule(noun)
        #print result
        if result:
            return result

def pluralize(noun):
    return plural(noun)

def singularize(word):
    specials = {
        "children" : "child",
        "mice"  : "mouse",
        "lice" : "louse",
        "men" : "man",
        "feet" : "foot",
        "women" : "woman"  
    }
    if word in specials.keys():
        return specials[word]
    # taken from:http://codelog.blogial.com/2008/07/27/singular-form-of-a-word-in-python/
    sing_rules = [lambda w: w[-3:] == 'ies' and w[:-3] + 'y',
              lambda w: w[-4:] == 'ives' and w[:-4] + 'ife',
              lambda w: w[-3:] == 'ves' and w[:-3] + 'f',
              lambda w: w[-2:] == 'es' and w[:-2],
              lambda w: w[-1:] == 's' and w[:-1],
              lambda w: w,
              ]
    word = word.strip()
    singleword = [f(word) for f in sing_rules if f(word) is not False][0]
    return singleword


def rel_dec(what, who):
    # We're going to return this decorator
    def simple_decorator(f):
        # This is the new function we're going to return
        # This function will be used in place of our original definition
        def wrapper():
            print(what)
            f()
            print(who)
        return wrapper
    return simple_decorator


#
# a class decorator that executes at import.
# ala flask app.route()
# does all the magic monkey patching stuff like:
#   * has_many
#   * setup the schema
#   * one to one
#   * many to many
#
# see: http://ains.co/blog/things-which-arent-magic-flask-part-1.html
# 
# For the relation part see: 
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class powDecNew():
    def __init__(self):
        self.relations = {}
    
    
    # below you can find the relation decorators
    # These types of relations are implementd:
    #   Functional notion       =>  sqlalchemy documentation notion
    # --------------------------------------------------------------------
    #   has_many_and_belongs_to =>  One To Many with backref
    #   has_many                =>  One To Many (without backref)
    #   belongs_to              =>  Many To One (without backref)
    #   one_to_one                 =>  One To One
    #   many_to_many            =>  Many To Many
    #   is_tree                 => Adjacence List
    #
    
    def has_many_and_belongs_to(self, child_as_str, backref=False):
       ##
       #
       #
       return self.has_many( child_as_str, backref=True)

    def has_many(self, child_as_str, backref=False):
        # cls is the class that has many of the related models (e.g. User, Post)
        # the "parent" class
        # rel_as_str is the plueral name of the child class (adresses, comments)
        # klass below is the real class instance of the child
        def decorator(parent_class):
            parent_name = parent_class.__name__.lower()
            parent_class_name = parent_class.__name__

            child_class_name = get_class_name(singularize(child_as_str))
            child_module_name = singularize(child_as_str)
            #print(sorted(locals().keys()))
            #print(sorted(globals().keys()))
            import sys
            if "{{appname}}.models.sql." + child_module_name in sys.modules.keys():
                #print(dir(sys.modules["{{appname}}.models.sql." + child_module_name]))
                child_klass = getattr(sys.modules["{{appname}}.models.sql." + child_module_name], child_class_name)
            else:
                import importlib
                mod = importlib.import_module('{{appname}}.models.sql.' + child_module_name)
                #mod = __import__('{{appname}}.models.sql.'+rel_module_name, fromlist=[rel_class_name])
                child_klass = getattr(mod, child_class_name)
            if backref:
                setattr(parent_class, child_as_str, relationship(child_class_name, 
                    order_by=child_klass.id,
                    back_populates=parent_name))
            else:
                setattr(parent_class, child_as_str, relationship(child_class_name))
            # prepare the include_attributes additions for the auto generated attrs
            setattr(parent_class, "include_attributes", getattr(parent_class,"include_attributes", []) + [child_as_str]  )

            setattr(child_klass, parent_name + "_id", Column(Integer, ForeignKey(pluralize(parent_name)+".id")))
            setattr(child_klass, "include_attributes", getattr(child_klass,"include_attributes", []) + [parent_name+"_id"]  )
            if backref:
                setattr(child_klass, parent_name, relationship(parent_class_name, back_populates=child_as_str))
                setattr(child_klass, "include_attributes", getattr(child_klass,"include_attributes", []) + [parent_name]  )
            ##print(dir(rel))
            print("RELATION: I see a: " + parent_class_name + " has many: " + child_as_str )
            if backref:
                print( "  .. and " + child_as_str + " belongs_to " + parent_name)
            return parent_class
        return decorator     
    
    def belongs_to(self, parent_as_str):
        # cls is the class that has many of the related models (e.g. User, Post)
        # the "parent" class
        # rel_as_str is the plueral name of the child class (adresses, comments)
        # klass below is the real class instance of the child
        def decorator(child_class):
            
            child_name = child_class.__name__.lower()
            parent_class_name = parent_as_str.capitalize()
            parent_module_name = parent_as_str
            parent_class = None
            import sys
            if ("{{appname}}.models.sql."+parent_module_name) in sys.modules.keys():
                parent_class = getattr(sys.modules["{{appname}}.models.sql."+parent_module_name], parent_class_name)
            else:
                import importlib
                mod = importlib.import_module('{{appname}}.models.sql.' + parent_module_name)
                #mod = __import__('{{appname}}.models.sql.'+rel_module_name, fromlist=[rel_class_name])
                parent_class = getattr(mod, parent_class_name)
            #print("parent_class: " + str(parent_class))
            #print(dir(klass))
            setattr(parent_class, child_name, relationship(child_class.__name__))
            setattr(parent_class, child_name + "_id", Column(Integer, ForeignKey(pluralize(child_name)+".id")))
            setattr(parent_class, "include_attributes", 
                getattr(parent_class,"include_attributes", []) + [child_name, child_name+"_id"]  )
            ##print(dir(rel))
            print("RELATION: I see a: " + child_name + " belongs_to: " + parent_as_str)
            return child_class
        return decorator

    def one_to_one(self, child_as_str):
        # cls is parent class (Post)
        # child_as_str is the singular name of the child (related class)
        # klass below is the real class instace of the child
        # one-to-one
        def decorator(parent):
            # cls is the parent class of the relation
            parent_name = parent.__name__.lower()
            #print("cls_name: " + cls_name)
            child_class_name = child_as_str.capitalize()
            child_module_name = child_as_str
            #print("child_class_name: " + child_class_name)
            #print("child_module_name: " + child_module_name)
            mod = __import__('{{appname}}.models.sql.'+child_module_name, fromlist=[child_class_name])
            klass = getattr(mod, child_class_name)
            #print("rel_class: " + str(klass))
            #print(dir(klass))
            setattr(parent, child_as_str, relationship(child_class_name, 
                uselist=False,
                back_populates=parent_name))
            setattr(parent, "include_attributes", 
                getattr(parent,"include_attributes", []) + [child_as_str]  )
            setattr(klass, parent_name + "_id", Column(Integer, ForeignKey(parent_name+".id")))
            setattr(klass, parent_name, relationship(parent_name.capitalize(), back_populates=child_as_str))
            setattr(klass, "include_attributes", 
                getattr(klass,"include_attributes", []) + [parent_name, parent_name + "_id"]  )
            ##print(dir(rel))
            print("RELATION: I see a: " + parent_name.capitalize() + " has many: " + child_as_str)
            return parent
        return decorator

    def many_to_many(self, children):
        # cls is the class that has many of the related models (e.g. User, Post)
        # the "parent" class
        # rel_as_str is the plueral name of the child class (adresses, comments)
        # klass below is the real class instance of the child
        from {{appname}}.database.sqldblib import Base
        def decorator(parent_class):
            parent_name = parent_class.__name__.lower()
            parent_class_name = parent_class.__name__
            
            #
            # create the new association Table and class
            #
            assoc_table = Table("association_" + parent_name + "_" + singularize(children),
                Base.metadata, 
                Column(parent_name + "_id", Integer, ForeignKey(pluralize(parent_name) + ".id")),
                Column(singularize(children)+"_id", Integer, ForeignKey(children + ".id"))
                )
            
            child_class_name = singularize(children).capitalize()
            child_module_name = singularize(children)

            #
            # set the parent attribute
            #
            setattr(parent_class, children, relationship(child_class_name, 
                secondary=assoc_table,
                back_populates=pluralize(parent_name)))
            # include_attrributes for to_dict() conversion
            setattr(parent_class, "include_attributes", 
                getattr(parent_class,"include_attributes", []) + [children]  )

            import sys
            if "{{appname}}.models.sql." + child_module_name in sys.modules.keys():
                #print(dir(sys.modules["{{appname}}.models.sql." + child_module_name]))
                child_klass = getattr(sys.modules["{{appname}}.models.sql." + child_module_name], child_class_name)
            else:
                import importlib
                mod = importlib.import_module('{{appname}}.models.sql.' + child_module_name)
                #mod = __import__('{{appname}}.models.sql.'+rel_module_name, fromlist=[rel_class_name])
                child_klass = getattr(mod, child_class_name)
            #
            # set the child attribute
            #
            setattr(child_klass, pluralize(parent_name), 
                relationship(parent_class_name, 
                    secondary=assoc_table, back_populates=children ))
            # include_attributes
            #setattr(child_klass, "include_attributes", 
            #    getattr(child_klass,"include_attributes", []) + [pluralize(parent_name)]  )
            ##print(dir(rel))
            print("RELATION: I see a: " + parent_class_name + " has many-to-many: " + children)
            return parent_class
        return decorator

    def is_tree(self):
        # cls is the class that has many of the related models (e.g. User, Post)
        # klass below is the real class instance of the child
        def decorator(cls):
            # parent is the parent class of the relation
            cls_name = cls.__name__.lower()
            #print(cls_name)
            setattr(cls, "parent_id", Column(Integer, ForeignKey(pluralize(cls_name)+".id")))
            setattr(cls, "children_list", relationship(cls_name.capitalize()))
            setattr(cls, "include_attributes", getattr(cls,"include_attributes", []) + ["children_list", "parent_id"]  )
            ##print(dir(rel))
            print("RELATION: I see a tree: " + cls_name.capitalize() )
            return cls
        return decorator

    def _many_to_one(self, child_as_str, backref=False):
        # parent is the class that has many of the related models (e.g. User, Post)
        # klass below is the real class instance of the child
        def decorator(parent):
            # parent is the parent class of the relation
            parent_name = parent.__name__.lower()
            #print("parent_name: " + parent_name)
            child_class_name = singularize(child_as_str).capitalize()
            child_module_name = singularize(child_as_str)
            child_table_name = child_class_name.lower()
            #print("child_class_name: " + child_class_name)
            #print("child_module_name: " + child_module_name)
            mod = __import__('{{appname}}.models.sql.'+child_module_name, fromlist=[child_class_name])
            klass = getattr(mod, child_class_name)
            #print("rel_class: " + str(klass))
            #print(dir(klass))
            setattr(parent, child_table_name + "_id", Column(Integer, ForeignKey(child_table_name + '.id')))
            setattr(parent, child_table_name, relationship(child_class_name))
            setattr(parent, "include_attributes", 
                getattr(parent,"include_attributes", []) + [child_table_name + "_id", child_table_name]  )
            if backref:
                setattr(klass, pluralize(parent_name), relationship(parent.__name__, back_populates=child_class_name))
                setattr(klass, "include_attributes", 
                    getattr(klass,"include_attributes", []) + [pluralize(parent_name)]  )
            ##print(dir(rel))
            print("RELATION: I see a: " + parent_name.capitalize() + " many to one: " + child_as_str)
            return parent
        return decorator

    def _one_to_many(self, child_as_str):
        # parent is the class that has many of the related models (e.g. User, Post)
        # klass below is the real class instance of the child
        def decorator(parent):
            # parent is the parent class of the relation
            parent_name = parent.__name__.lower()
            #print("parent_name: " + parent_name)
            child_class_name = singularize(child_as_str).capitalize()
            child_module_name = singularize(child_as_str)
            #print("child_class_name: " + child_class_name)
            #print("child_module_name: " + child_module_name)
            mod = __import__('{{appname}}.models.sql.'+child_module_name, fromlist=[child_class_name])
            klass = getattr(mod, child_class_name)
            #print("rel_class: " + str(klass))
            #print(dir(klass))
            setattr(parent, child_as_str, relationship(child_class_name))
            setattr(klass, parent_name + "_id", Column(Integer, ForeignKey(pluralize(parent_name)+".id")))
            # include_attributes
            setattr(parent, "include_attributes", 
                    getattr(parent,"include_attributes", []) + [child_as_str]  )
            setattr(klass, "include_attributes", 
                    getattr(klass,"include_attributes", []) + [parent_name + "_id"]  )
            ##print(dir(rel))
            print("RELATION: I see a: " + parent_name.capitalize() + " has many: " + child_as_str)
            return parent
        return decorator
    #
    # sets up a sqlqlchemy schema from a cerberus schema dict
    # goal is to go seamlessly to NoSql AND to bring validation in
    # the schema definition at once!
    # ONE definition for SQL, NoSQL and Validation.
    # 
    def setup_sql_schema(self, what=""):
        def decorator(cls):
            print("setup_schema:" + cls.__name__.lower())
            #
            # create a sqlalchemy model from the schema
            #
            # there are two special keys you can use additionally to the
            # standard cerberus syntx:
            # "sql" :   add any Column __init__ kwargs here, they will be handed raw
            #           to the Column __init__
            # "sqltype":    specify a more precise SQL subtype.
            #               e.g. cerberus has integer. SQL has INTEGER, BIGINTEGER
            # the two special keys will be removed from the schema at the end of this
            # decorator.
            #    
            colclass = None
            
            from sqlalchemy import Column, Integer, String, Date, DateTime, Float
            from sqlalchemy import Unicode, Text, Boolean, Numeric, BigInteger, LargeBinary
            #
            # now set the right sqlalchemy type for the column
            #
            for elem in cls.schema.keys():
                #print(elem)
                # the raw Column __init__ parameters dict
                sql=cls.schema[elem].get("sql", {})
                if cls.schema[elem]["type"] == "integer":
                    if "sqltype" in cls.schema[elem]:
                        if cls.schema[elem]["sqltype"].lower() == "biginteger":
                            setattr(cls, elem, Column(elem, BigInteger, **sql))
                    else:
                        setattr(cls, elem, Column(elem, Integer, **sql))
                elif cls.schema[elem]["type"] == "float":
                    setattr(cls, elem, Column(elem, Float, **sql))
                elif cls.schema[elem]["type"] == "string":
                    if "sqltype" in cls.schema[elem]:
                        if cls.schema[elem]["sqltype"].lower() == "text":
                                setattr(cls, elem, Column(elem, Text, **sql))
                        elif cls.schema[elem]["sqltype"].lower() == "unicode":
                            if "maxlength" in cls.schema[elem]:
                                setattr(cls, elem, Column(elem, Unicode(length=cls.schema[elem]["maxlength"]), **sql))
                            else:
                                setattr(cls, elem, Column(elem, Unicode, **sql))
                    else:    
                        if "maxlength" in cls.schema[elem]:
                            setattr(cls, elem, Column(elem, String(length=cls.schema[elem]["maxlength"]), **sql))
                        else:
                            if "allowed" in cls.schema[elem]:
                                strmax = max(cls.schema[elem]["allowed"], key=len)
                                print("setting max stringlength to: "+ str(len(strmax)))
                                setattr(cls, elem, Column(elem, String(length=len(strmax)), **sql))
                            else:
                                setattr(cls, elem, Column(elem, String, **sql))
                elif cls.schema[elem]["type"] == "boolean":
                    setattr(cls, elem, Column(elem, Boolean, **sql))
                elif cls.schema[elem]["type"] == "date":
                    setattr(cls, elem, Column(elem, Date, **sql))
                elif cls.schema[elem]["type"] == "datetime":
                    setattr(cls, elem, Column(elem, DateTime, **sql))
                elif cls.schema[elem]["type"] == "number":
                    setattr(cls, elem, Column(elem, Numeric, **sql))
                elif cls.schema[elem]["type"] == "binary":
                    setattr(cls, elem, Column(elem, LargeBinary, **sql))
                else:
                    raise Exception("Wrong Datatype in schema") 
                #print("  .. removing the schema (raw) sql key(s)")
                cls.schema[elem].pop("sql", None)
                cls.schema[elem].pop("sqltype", None)
        
            return cls
        return decorator

    #
    # sets up an elastic DSLschema from a cerberus schema dict
    # goal is to go seamlessly to NoSql AND to bring validation in
    # the schema definition at once!
    # ONE definition for SQL, NoSQL and Validation.
    # See: http://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html
    def setup_elastic_dsl_schema(self, what=""):
        def decorator(cls):
            print("setup_schema:" + cls.__name__.lower())
            #
            # create an elastic model from the schema
            #
            # there are two special keys you can use additionally to the
            # standard cerberus syntx:
            # "elastic" :   add any Elastic DSL "Column" __init__ kwargs here, they will be handed raw
            #               to the Column __init__
            # "elastictype" : add a more specific elasticserach_dsl type definition (Text instead of string)
            # the two special keys will be removed from the schema at the end of this
            # decorator.
            #    

            #
            # now set the right elastic types for the doc
            #
            from datetime import datetime
            #from elasticsearch_dsl import DocType, String, Date, Nested, Boolean, Integer            #    Float, Byte, Text, analyzer, InnerObjectWrapper, Completion
            import elasticsearch_dsl
            
            for elem in cls.schema.keys():
                #print(elem)
                # the raw Column __init__ parameters dict
                elastic=cls.schema[elem].get("elastic", {})
                if cls.schema[elem]["type"] == "integer":
                    setattr(cls, elem, elasticsearch_dsl.Integer(**elastic))
                elif cls.schema[elem]["type"] == "float":
                    setattr(cls, elem, elasticsearch_dsl.Float(**elastic))
                elif cls.schema[elem]["type"] == "string":
                    setattr(cls, elem, elasticsearch_dsl.Text(**elastic))
                elif cls.schema[elem]["type"] == "bool":
                    setattr(cls, elem, elasticsearch_dsl.Boolean(**elastic))
                elif cls.schema[elem]["type"] == "date":
                    setattr(cls, elem, elasticsearch_dsl.Date(**elastic))
                elif cls.schema[elem]["type"] == "datetime":
                    setattr(cls, elem, elasticsearch_dsl.Date(**elastic))
                elif cls.schema[elem]["type"] == "number":
                    setattr(cls, elem, elasticsearch_dsl.Integer(**elastic))
                elif cls.schema[elem]["type"] == "binary":
                    setattr(cls, elem, elasticsearch_dsl.Byte(**elastic))
                elif cls.schema[elem]["type"] == "list":
                    setattr(cls, elem, elasticsearch_dsl.Keyword(**elastic))
                else:
                    raise Exception("Wrong Datatype in schema") 
                #print("  .. removing the schema (raw) elastic key(s)")
                cls.schema[elem].pop("elastic", None)
                cls.schema[elem].pop("elastictype", None)

            return cls
        return decorator

relation = powDecNew()


