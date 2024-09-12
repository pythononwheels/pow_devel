#
# TinyDB Model:  User
#
from {{appname}}.models.tinydb.basemodel import TinyBaseModel

class User(TinyBaseModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    #
    schema = {
        'login': {'type': 'string'},
        'password': {'type': 'string', 'maxlength' : 35},
        
    }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here