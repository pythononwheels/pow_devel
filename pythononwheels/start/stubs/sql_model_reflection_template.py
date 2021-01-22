#
# Model Uidtest
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
    
    schema = {}
    
    # if you dont want to use the pow schema extension
    _use_pow_schema_attrs= False

    # define class attributes/variables here that should be included in to_dict() 
    # conversion and also handed to the encoders but that are NOT part of the schema.
    include_attributes=[]
    
    __tablename__ = "<your tablename here>"
    
    __table__ = Table(
        '<your tablename here>',
        Base.metadata,
        #PrimaryKeyConstraint("id", name="pk_id"),  #if you want to tweak a column explicitly e.g. making it primary key
        autoload_with=engine    # turn on reflection
    )
    
    #
    # init
    #
    def __init__(self, **kwargs):
        self.setup_instance_values()
        self.init_on_load(**kwargs)
        
    #
    # your model's methods down here
    #
