#
# Model {{model_class_name}}
#
from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy import BigInteger, Date, DateTime, Float, Numeric, Unicode, Text
from {{appname}}.powlib import relation
from {{appname}}.database.sqldblib import Base 

#@relation.has_many("<plural_other_models>")
@relation.setup_sql_schema()
class {{model_class_name}}(Base):
    
    #
    # cerberus style schema
    #
    schema = {        
        'title' :   { 'type' : 'string', 'maxlength' : 35 },
        'text'  :   { 'type' : 'string' },
        "votes" :   { "type" : "integer", "default" : 0 }  
    }

    # define a custom tablename to link for this model:
    #__tablename__ = "{{model_name_plural}}"
    
    # define class attributes/variables here that should be included in to_dict() 
    # conversion and also handed to the encoders but that are NOT part of the schema.
    include_attributes=[]

    # Add sqlalchemy table_args here. Add "autoload" : True for reflection
    __table_args__ = { "extend_existing": True  }
    
    #
    # init
    #
    def __init__(self, **kwargs):
        self.setup_instance_values()
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
