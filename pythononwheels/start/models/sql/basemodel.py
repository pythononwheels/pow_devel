import os
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.expression import func 
from {{appname}}.database.sqldblib import engine,session
from {{appname}}.powlib import pluralize
import datetime
import uuid
from sqlalchemy import orm
import sqlalchemy.inspection
from cerberus import Validator
import xmltodict
import simplejson as json
import datetime, decimal
from {{appname}}.config import myapp
import {{appname}}.config as cfg
from {{appname}}.models.modelobject import ModelObject
from {{appname}}.config import database as dbcfg
#print ('importing module %s' % __name__)

def make_uuid():
    """
        dummy function to test uuid default value.
    """
    return str(uuid.uuid4())

class SqlBaseModel(ModelObject):
    """
        All the basic stuff for SQL Models.
        Defaults, init functions, observers, querys
        upsert, delete, 
        init_from (json, xml,csv ...)
        printing
        ...
        all the stuff you dont need to implement.

    """
    #__table_args__ = { "extend_existing": True }
    
    #id =  Column(Integer, primary_key=True)
    # #_uuid = Column(String, default=make_uuid)
    # # create_date column will be populated with the result of the now() SQL function 
    # #(which, depending on backend, compiles into NOW() or CURRENT_TIMESTAMP in most cases
    # # see: http://docs.sqlalchemy.org/en/latest/core/defaults.html
    #created_at = Column(DateTime, default=func.now())
    #last_updated = Column(DateTime, onupdate=func.now(), default=func.now())
    session = session

    @orm.reconstructor
    def init_on_load(self, *args, **kwargs):
        #
        # setup a mashmallow schema to be able to dump (serialize) and load (deserialize)
        # models to json quick, safe and easy.
        # see: http://marshmallow-sqlalchemy.readthedocs.io/en/latest/
        # and link it to the model. (as jsonify attribute)
        # this enables the model to load / dump json
        # 
        #print(kwargs)
        self.class_name = self.__class__.__name__.capitalize()
        from marshmallow_sqlalchemy import ModelSchema
        cls_meta=type("Meta", (object,),{"model" : self.__class__})
        
        jschema_class = type(self.class_name+'Schema', (ModelSchema,),
                {
                    "Meta": cls_meta,
                    "model" : self.__class__,
                    #"sqla_session" : session   
                }
            )
        setattr(self, "marshmallow_schema", jschema_class())
        self.session=session
        
        #
        # set the tablename
        #
        #if getattr(self.__class__, "_tablename", None):
        #    self.table = self.metadata.tables[getattr(self.__class__, "_tablename")]
        #else:    
        #    self.table = self.metadata.tables[pluralize(self.__class__.__name__.lower())]
        #self.__class__._tablename = self.table.name
        self.table = self.metadata.tables[self.__class__.__tablename__]
        
        #
        # if there is a schema (cerberus) set it in the instance
        #
        #print(str(self.__class__.__dict__.keys()))
        if "schema" in self.__class__.__dict__:
            #print(" .. found a schema for: " +str(self.__class__.__name__) + " in class dict")
            self.schema = self.__class__.__dict__["schema"]
        # add the sqlcolumns schema definitions to the cerberus schema (if there are any)
        if myapp["sql_auto_schema"]:
            self._setup_schema_from_sql()
            
        #self.setup_instance_values()
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
        self.init_observers()
        #elf.setup_dirty_model()
        

    @declared_attr
    def __tablename__(cls):
        """ 
            returns the tablename for this model. Convention: pluralized Modelname
            You can overwrite this by just setting the __tablename__ = <yourtablename> in the
            model class.
        """
        return pluralize(cls.__name__.lower())
        
    #def set_table(self, name):
    #    """  setting the table for this model directly. (Not used: see _custom_tablename parameter) """
    #    # setting the tablename
    #    self.table = self.metadata.tables[name]
    
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
                    if key not in ["created_at", "last_updated", "id"]:
                        setattr(self,key,cfg.database["default_values"][self.schema[key]["type"]])
                except Exception as e:
                    print(e.message)
                    setattr(self, key, None)

    def _setup_schema_from_sql(self):
        """
            Constructs a cerberus definition schema 
            from a given sqlalchemy column definition
            for this model.
        """
        #print(" .. setup schema from sql for : " + str(self.class_name))
        for idx,col in enumerate(self.table.columns.items()):
            # looks like this: 
            # ('id', 
            #  Column('id', Integer(), table=<comments>, primary_key=True, 
            #     nullable=False))
            col_type = col[1].type.python_type
            col_name = str(col[0])
            exclude_list = [elem for elem in self.schema.keys()]
            #exclude_list.append( ["id", "created_at", "last_updated"] )
            #print("    #" + str(idx) + "->" + str(col_name) + " -> " + str(col_type))
            # dont check internal columns or relation columns.
            #print(str(col[1].foreign_keys))
            # col[0] is the column name
            # col[1] is the sqlalchemy.Column object
            if ( col_name not in exclude_list ) and ( len(col[1].foreign_keys) == 0 ): 
                #print("  .. adding to schema: " + col_name)  
                if col_type == int:
                    # sqlalchemy: Integer, BigInteger
                    # cerberus: integer
                    self.schema[col_name] = { "type" : "integer" }
                elif col_type == str:
                    # sqlalchemy: String, Text
                    # cerberus: string
                    # python: str
                    self.schema[col_name] = { "type" : "string" }
                elif col_type == bool:
                    # sqlalchemy: Boolean
                    # cerberus: boolean
                    # python: bool
                    self.schema[col_name] = { "type" : "boolean" }
                elif col_type == datetime.date:
                    # sqlalchemy: Date
                    # cerberus: date
                    # python: datetime.date
                    self.schema[col_name] = { "type" : "date" }
                elif col_type == datetime.datetime:
                    # sqlalchemy: DateTime
                    # cerberus: datetime
                    # python: datetime.datetime
                    self.schema[col_name] = { "type" : "datetime" }
                elif col_type == float:
                    # sqlalchemy: Float
                    # cerberus: float
                    # python: float
                    self.schema[col_name] = { "type" : "float" }
                elif col_type == decimal.Decimal:
                    # sqlalchemy: Numeric
                    # cerberus: number
                    # python: decimal.Decimal
                    self.schema[col_name] = { "type" : "number" }
                elif col_type == bytes:
                    # sqlalchemy: LargeBinary
                    # cerberus: binary
                    # python: bytes
                    self.schema[col_name] = { "type" : "binary" }
            else:
                #print("  .. skipping: " + col_name )
                pass
                
    # def init_from_json(self, data, ignore=False, autoconvert=True):
    #     """
    #         makes a py dict from input json and
    #         sets the instance attributes 
    #     """

    #     print("  ..  marshmallow load data input: " + str(data))
    #     if not isinstance(data,(dict)):
    #         data=json.loads(data)
    #     d=self.marshmallow_schema.load(data, session=session).data
    #     print("  . .. init_from_json returned Model d: " + str(d))
    #     print("  . .. init_from_json returned Model d type: " + str(type(d)))
    #     self.__dict__ = d.__dict__
    #     return 
    
    def to_json(self):
        return json.dumps(self.marshmallow_schema.dump(self).data)

    # def json_dumps(self):
    #     """ probably better return str(self.json_dump()) ??... test it """
    #     return json.dumps(self.json_dump())

    # def json_dump(self):
    #     """ return this instances columns as json"""
    #     return self._jsonify.dump(self).data
   
    def json_load_from_db(self, data, keep_id=False):
        if keep_id:
            self = self._jsonify.load(data, session=session).data
            return self
        else:
            obj = self.__class__()
            obj = obj._jsonify.load(data, session=session).data
            obj.id = None
            return obj
    
    def json_result_to_object(self, res):
        """
            creates a list of instances of this model 
            from a given json resultlist
        """
        if not isinstance(res,(list)):
            #single element, pack it in a list
            res = [res]
        # lists, iterate over all elements
        reslist = []
        for elem in res:
            m = self.__class__()
            #print(str(type(elem)) + "->" + str(elem))
            m.init_from_json(elem)
            #print("adding model to reslist: " + str(m))
            reslist.append(m)
        return reslist
    
    def get_relationships(self):
        """
            returns the raw relationships
            see: http://stackoverflow.com/questions/21206818/sqlalchemy-flask-get-relationships-from-a-db-model
        """
        return sqlalchemy.inspection.inspect(self.__class__).relationships

    def get_relations(self):
        """
            returns a list of the relation names
            see: http://stackoverflow.com/questions/21206818/sqlalchemy-flask-get-relationships-from-a-db-model
        """
        rels = sqlalchemy.inspection.inspect(self.__class__).relationships
        return rels.keys()
    
    def sync(self):
        self.session.expire(self)
        self.session.refresh(self)
    
    def new_session(self):
        """
            create an entirely new session
        """
        from sqlalchemy.orm import sessionmaker
        self.session = sessionmaker(bind=engine)()


    def _rep_model_as_str(self):
        """
            returns a string with the models columns 
            and value information
            including realtion, keys etc..
        """
        line = ""
        for a in self.__mapper__.attrs:
            if isinstance(a, orm.properties.ColumnProperty):
                c = a.columns[0]
                line += '{:20}'.format(a.key)
                line += ": " + str(getattr(self, a.key))
                if c.primary_key:
                    line += '{:15}'.format(" (primary key)")
                if c.foreign_keys:
                    for k in c.foreign_keys:
                        line += '{:20}'.format(" (" + k.target_fullname + ")")
                    #line += ' {:40}'.format(", ".join([fk.target_fullname for fk in c.foreign_keys]))
                line += os.linesep
            elif isinstance(a, orm.properties.RelationshipProperty):
                line += "{:20}: {} relationship with <model {}>".format(a.key, a.direction.name, a.mapper.class_.__name__)
                line += os.linesep

        return line
    def __repr__(self):
        """
            __repr__ method is what happens when you look at it with the interactive prompt
            or (unlikely: use the builtin repr() function)
            usage: at interactive python prompt
            p=Post()
            p
            see: http://stackoverflow.com/questions/26147410/what-is-a-good-way-to-pretty-print-a-sqlalchemy-database-as-models-and-relations
        """
        # odict = {}
        # for a in self.__mapper__.attrs:
        #     if isinstance(a, orm.properties.ColumnProperty):
        #         c = a.columns[0]
        #         line = a.key
        #         line += str(getattr(self, a.key))
        #         if c.primary_key:
        #             line += " (primary key)"
        #         if c.foreign_keys:
        #             line += " -> " + ", ".join([fk.target_fullname for fk in c.foreign_keys])
        #         print(line)
        #     elif isinstance(a, orm.properties.RelationshipProperty):
        #         print ("{} -> {} relationship with <model {}>".format(
        #             a.key, a.direction.name, a.mapper.class_.__name__))
        # return ""
        return self._rep_model_as_str()
        

    def print_full(self):
        #
        # prints everything including related objects in FULL
        # lenghty but you see everything.
        #
        from pprint import pformat
        d = {}
        for k in self.__dict__.keys():
            if not k.startswith("_"):
                d[k] = self.__dict__.get(k)

        # add the related objects:
        for elem in self.get_relations():
            #print(elem)
            d[elem] = str(getattr(self, elem))

        return pformat(d,indent=4)
            
            
    def create_table(self):
        """
            creates the physical table in the DB
        """
        self.__table__.create(bind=engine)

    def drop_table(self):
        """
            drops the physical table in the DB
        """
        self.__table__.drop(bind=engine)
    
    def upsert(self, session=None):
        """
            intelligently updates or inserts the elememt 
        """
        if self.observers_initialized:
            for observer in self.observers:
                try:
                    ret = observer.before_upsert(self)
                except:
                    pass
        
        self.session.add(self)
        self.session.commit()
        if self.observers_initialized:
            for observer in self.observers:
                try:
                    ret = observer.after_upsert(self)
                except Exception as e:
                    print(str(e))    
        # clean the dirty marks. 
        #self.dirty = {}
        #self.is_dirty = False    
        #session.flush()
    
    def delete(self, session=None):
        """
            deltest the element from the db
        """
        if self.observers_initialized:
            for observer in self.observers:
                try:
                    ret = observer.before_delete(self)
                except:
                    pass
        
        self.session.delete(self)
        self.session.commit()        
        #session.flush()
        
        # clean the dirty marks. 
        #self.dirty = {}
        #self.is_dirty = False 

        if self.observers_initialized:
            for observer in self.observers:
                try:
                    ret= observer.after_delete(self)
                except:
                    pass
        

    

    def find_from_statement(self, statement):
        """
            Executes a given SQL query statement
        """
        return session.query(self.__class__).from_statement(statement)

    def page(self, *criterion, page=0, page_size=None):
        """ return the next page of results. See config["myapp"].page_size 
            actually means: (taking the sql understandng)
                 page === offset 
                 limit === limit
        """
        if page_size == None:
            page_size = myapp["page_size"]
        if cfg.database["sql"]["type"] == "sqlite":
             limit=page_size
        else:
             limit=(page*page_size)+page_size
        res = self.find_all( 
             limit=limit,
             offset=page*page_size
             )
        #res = session.query(self.__class__).filter(*criterion).limit(limit).offset(offset).all()
        return res

    def find(self,*criterion):
        """
            Executes a find operation.
            Example: model.find(ModelClass.attribute == "someval")
                     p.find(Post.title=="first")
        """
        self.session.expire_all()
        return self.session.query(self.__class__).filter(*criterion).yield_per(dbcfg["sql"]["yield_per"])
    
    def find_by_id(self, id):
        """
            Searches the DB by id
        """
        self.session.expire_all()
        return self.session.query(self.__class__).get(id)

    def find_all(self, *criterion, raw=True, limit=None, offset=None):
        """
            Searches the DB (Parameters: limit, offset ..)
            Returns a sqlalchemy.orm.query.Query object (raw=True)
            Or a list of PoW Model instances (raw=False)

            See get_all also.
        """
        self.session.expire_all()
        if raw:
            return self.session.query(self.__class__).filter(*criterion).yield_per(dbcfg["sql"]["yield_per"]).limit(limit).offset(offset)
        res = self.session.query(self.__class__).filter(*criterion).limit(limit).offset(offset).yield_per(dbcfg["sql"]["yield_per"]).all()
        return res
    
    def count(self,*criterion):
        """ same as model.find_all(criterion).count()   """
        return self.find_all(*criterion).count()
    
    def get_max(self, column, as_scalar=True):
        """
            returns the max val of a column as scalar()
            or as a query (if as_scalar == False )
        """
        if as_scalar:
            return self.session.query(func.max(column)).scalar()
        else:
            return self.session.query(func.max(column))

    def get_all(self):
        """ returns all elements without any filters as a list of PoW models"""
        return self.find_all(raw=True)

    def find_one(self, *criterion):
        """
            returns one or none
        """
        self.session.expire_all()
        res = self.session.query(self.__class__).filter(*criterion).one()
        return res

    def find_first(self, *criterion):
        """
            return the first match (if any)
        """
        self.session.expire_all()
        res = self.session.query(self.__class__).filter(*criterion).first()
        return res

    def q(self):
        """ return a raw sqlalchemy query object """
        return self.session.query(self.__class__)

    def find_dynamic(self, filter_condition = [('name', 'eq', 'klaas')]):
        """
            create a dynamic filter like this: [('name', 'eq', 'klaas')]
                filter_condition = [('name', 'eq', 'klaas')]
        """
        
        dynamic_filtered_query_class = DynamicFilter(query=None, model_class=self,
                                  filter_condition=filter_condition)
        dynamic_filtered_query = dynamic_filtered_query_class.return_query()
        return dynamic_filtered_query

class DynamicFilter():
    def __init__(self, query=None, model_class=None, filter_condition=None):
        
        #super().__init__(*args, **kwargs)
        self.query = query
        self.model_class = model_class.__class__
        self.filter_condition = filter_condition
        self.session = get_session()


    def get_query(self):
        '''
        Returns query with all the objects
        :return:
        '''
        if not self.query:
            self.query = self.session.query(self.model_class)
        return self.query


    def filter_query(self, query, filter_condition):
        '''
        Return filtered queryset based on condition.
        :param query: takes query
        :param filter_condition: Its a list, ie: [(key,operator,value)]
        operator list:
            eq for ==
            lt for <
            ge for >=
            in for in_
            like for like
            value could be list or a string
        :return: queryset
        '''

        if query is None:
            query = self.get_query()
        #model_class = self.get_model_class()  # returns the query's Model
        model_class = self.model_class
        for raw in filter_condition:
            try:
                key, op, value = raw
            except ValueError:
                raise Exception('Invalid filter: %s' % raw)
            column = getattr(model_class, key, None)
            if not column:
                raise Exception('Invalid filter column: %s' % key)
            if op == 'in':
                if isinstance(value, list):
                    filt = column.in_(value)
                else:
                    filt = column.in_(value.split(','))
            else:
                try:
                    attr = list(filter(
                        lambda e: hasattr(column, e % op),
                        ['%s', '%s_', '__%s__']
                    ))[0] % op
                except IndexError:
                    raise Exception('Invalid filter operator: %s' % op)
                if value == 'null':
                    value = None
                filt = getattr(column, attr)(value)
            query = query.filter(filt)
        return query


    def return_query(self):
        return self.filter_query(self.get_query(), self.filter_condition)