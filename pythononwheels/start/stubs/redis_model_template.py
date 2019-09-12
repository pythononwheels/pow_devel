#
# Redis Model
#
from {{appname}}.models.redis.basemodel import RedisBaseModel
from datetime import datetime


class {{model_class_name}}(RedisBaseModel):
    #
    # Use the cerberus schema style 
    # which offer you an Elastic schema and
    # immediate validation with cerberus
    #

    schema = {
        'title'     : { 'type': 'string' },
        'text'      : { 'type': 'string', 'maxlength' : 235 },
        'tags'      : { 'type': 'list' },
        'votes'     : { "type": 'integer' }
    }

    #
    # your model's methods down here
    #
    def __init__(self, *args, **kwargs):
        self.init_on_load()