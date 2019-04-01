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
    # You can use column definitions in sqlalchemy classic style
    # which offer you all sqlalchemy options
    #
    # title = Column(String(50))
    # text = Column(String)
    
    #
    # Or use the new preferred cerberus schema style 
    # which offer you immediate validation with cerberus
    # with the special "sql" key you can hand Over
    # raw sqlalchemy column __init__ parameters.
    #
    schema = {        
        'title' :   { 'type' : 'string', 'maxlength' : 35 },
        'text'  :   { 'type' : 'string' },
        "votes" :   { "type" : "integer", "default" : 0 }  
    }

    # you can also use special sqlalchemy attributes which are handed raw ro sqlalchemy. 
    #       => (see "sql" parameter)
    # and for type string (default varchar) you can specify the concrete sql type 
    # currently text or unicode =>   (see "sqltype")
    # like this:
    #
    # schema = {        
    #     'title': {'type': 'string', 'maxlength' : 35},
    #     'text': {'type': 'string', "sqltype" : "text" }, 
    #     'likes': {
    #         'type': 'integer',
    #          "sql" : {          # sql attributes are handed raw to sqlalchemy Column
    #             "primary_key"   : False,
    #             "default"       : "123",
    #             "unique"        : False, 
    #             "nullable"      : False 
    #         }
    #     }
    # }

    
    # define class attributes/variables here that should be included in to_dict() 
    # conversion and also handed to the encoders but that are NOT part of the schema.
    include_attributes=[]

    # Add sqlalchemy table_args here.
    #__table_args__ = { "autoload" : True  }

    # init
    def __init__(self, **kwargs):
        self.setup_instance_values()
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
