#
# Model
#
from {{appname}}.lib.powlib import relation
from {{appname}}.sqldblib import Base 

#@relation.has_many('childs')
@relation.setup_sql_schema()
class Parent(Base):
    # https://media.readthedocs.org/pdf/cerberus/latest/cerberus.pdf
    # you can use directly mapped to db types: (SQL AND NoSQL)
    #    cerberus           sqlalchemy
    # ----------------------------------------
    #    integer            Integer
    #    float              Float
    #    string             Unicode
    #                       Text (ohne Limit)
    #    bool               Boolean
    #    datetime           DateTime
    #    date               Date
    #    number             Numeric
    #    
    # lists have to be handled through @relations.has_many or many_to_many
    # 
    schema = {
        # string sqltypes can be TEXT or UNICODE or nothing
        'name': {'type': 'string', 'maxlength' : 35},
        'text': {'type': 'string'},
        'unicode' : {'type' : 'string'},
        
        # sqltype: BIGINTEGER and SMALLINTEGER are possible
        'test2': {'type': 'integer','min' : 10, 'max' : 100},
        
        'test3': {'type': 'float'}

        }
    # init
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)