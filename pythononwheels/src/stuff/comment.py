#
# Model Comment
#
from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy import BigInteger, Date, DateTime, Float, Numeric
from pow_comments.powlib import relation
from pow_comments.sqldblib import Base 

#@relation.has_many("<plural_other_models>")
@relation.is_tree()
@relation.setup_schema()
class Comment(Base):
    #
    # put your column definition here:
    #
    # 
    # sqlalchemy classic style
    # which offer you all sqlalchemy options
    #
    #title = Column(String(50))
    #text = Column(String)
    
    #
    # or the new (cerberus) schema style 
    # which offer you immediate validation 
    #
    schema = {
        # string sqltypes can be TEXT or UNICODE or nothing
        'author': {
            'type': 'string', 'maxlength' : 35,
            # the sql "sub"key lets you declare "raw" sql(alchemy) Column options
            # the options below are implemented so far.
            "sql" : {
                "primary_key" : False,
                "default"   : "No Author Name",
                "unique"    : True, 
                "nullable"  : False 
            }
        },
        'text': {'type': 'string'}
    }

    # init
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)

    # your methods down here
