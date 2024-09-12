#
# Model
#
from sqlalchemy import Column, Integer, String, Sequence, Text
from {{appname}}.lib.powlib import relation
from {{appname}}.database.sqldblib import Base 

#@relation.many_to_many("groups")
class User(Base):
    login = Column(String)
    password = Column(String)
    

    # these are just for test purposes 
    # todo: remove before release
    #num = Column(Numeric)
    #bin = Column(LargeBinary)
    #email = Column(String)
    #test = Column(Text)
    
    schema={}
    # init
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)

    # your methods down here