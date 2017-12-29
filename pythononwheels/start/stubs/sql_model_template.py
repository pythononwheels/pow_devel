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
    #title = Column(String(50))
    #text = Column(String)
    
    #
    # Or use the new preferred cerberus schema style 
    # which offer you immediate validation with cerberus
    # with the special "sql" key you can hand Over
    # raw sqlalchemy column __init__ parameters.
    #
    schema = {        
        'title' :   {'type': 'string', 'maxlength' : 35},
        'text'  :   {'type': 'string'},
        "votes" :   { "type" : "integer", "default" : 0 }  
    }

    # you can also use special sqlalchemy attributes which are handed raw ro sqlalchemy
    # like this:
    # schema = {        
    #     'title': {'type': 'string', 'maxlength' : 35},
    #     'text': {'type': 'string'},
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


    #__table_args__ = { "autoload" : True  }

    # init
    def __init__(self, **kwargs):
        self.setup_instance_values()
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
