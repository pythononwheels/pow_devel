#
# Model {{model_class_name}}
#
from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy import BigInteger, Date, DateTime, Float, Numeric, Unicode, Text
from sqlalchemy import PrimaryKeyConstraint, Table
from {{appname}}.lib.powlib import relation
from {{appname}}.database.sqldblib import Base, engine
from {{appname}}.lib.powlib import PowBaseMeta

#@relation.has_many("<plural_other_models>")
@relation.setup_sql_schema()
class {{model_class_name}}(Base, metaclass=PowBaseMeta):
    
    #
    # cerberus style schema
    # schema = {} when using reflection
    #
    schema = {        
        'title' :   { 'type' : 'string', 'maxlength' : 35 },
        'text'  :   { 'type' : 'string' },
        "votes" :   { "type" : "integer", "default" : 0 }  
    }

    # if you want to define a custom tablename for this model set it here.
    # remark: when using reflection always set the __tablename__ explicitly
    __tablename__ = "{{model_name_plural}}"
    
    # if you dont want to use the pow schema extension, set this to: False
    # when using reflection you probably want to set this to False. 
    _use_pow_schema_attrs= True

    # define class attributes/variables here that should be included in to_dict() 
    # conversion and also handed to the encoders but that are NOT part of the schema.
    include_attributes=[]

    # Add sqlalchemy table_args here. Add "autoload" : True for database reflection
    __table_args__ = { "extend_existing": True  }

    # or use this instead of__table_args__ to have a more finegrained control
    # __table__ = Table(
    #     '<tablename>',
    #     Base.metadata,
    #     PrimaryKeyConstraint("id", name="pk_id"), # set col primary_key if the original table does not have a pk col
    #     autoload_with=engine
    # )
    
    #
    # init
    #
    def __init__(self, **kwargs):
        self.setup_instance_values()
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
