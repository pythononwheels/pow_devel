#
# Elastic Model:  Testelastic
#
from {{appname}}.models.elastic.basemodel import ElasticBaseModel
from {{appname}}.database.elasticdblib import dbname
from datetime import datetime


class {{model_class_name}}(ElasticBaseModel):
    #
    # Use the cerberus schema style 
    # which offer you an Elastic schema and
    # immediate validation with cerberus
    #

    schema = {
        'title'     : { 'type': 'string' },
        'body'      : { 'type': 'string', 'maxlength' : 235 },
        'tags'      : { 'type': 'list' },
        'published_from' : { "type": 'date' },
        'lines' : { "type": 'integer' }
    }

    #
    # your model's methods down here
    #
    def save(self, ** kwargs):
        if getattr(self, body, None):
            self.lines = len(self.body.split())
        self.upsert()
