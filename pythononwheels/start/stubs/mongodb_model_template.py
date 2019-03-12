#
# MongoDB Model:  {{model_class_name}}
#
from {{appname}}.models.mongodb.mongomodel import MongoModel

class {{model_class_name}}(MongoModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        'title' :   { 'type' : 'string', 'maxlength' : 35 },
        'text'  :   { 'type' : 'string' },
        'tags'  :   { 'type' : 'list', "default" : [] },
        "votes" :   { "type" : "integer", "default" : 0 }   
        }

    # define class attributes/variables here that should be included in to_dict() 
    # conversion and also handed to the encoders but that are NOT part of the schema.
    include_attributes=[]
    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
