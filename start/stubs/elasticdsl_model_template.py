#
# Elastic Model:  Testelastic
#
from elasticsearch_dsl import Date, Boolean, Text, Integer, Byte, Float, Keyword
from {{appname}}.models.elastic.dsl_basemodel import ElasticDSLBaseModel
from {{appname}}.powlib import relation
from elasticsearch_dsl import DocType
from {{appname}}.database.elasticdblib import dbname
from datetime import datetime


@relation.setup_elastic_dsl_schema()
class {{model_class_name}}(ElasticBaseModel):

    #
    # Use the cerberus schema style 
    # which offer you an ElasticDSL schema and
    # immediate validation with cerberus
    #
    class Meta:
        index =  dbname

    schema = {
        'title': {
            'type': 'string',
            "elastic" : {    
                "analyzer"  : "snowball",
                "fields"    : {'raw': Keyword()}
            }
        },
        'body': {
            'type': 'string', 'maxlength' : 235,
            "elastic" : {    
                "analyzer"  : "snowball"
            }
        },
        'tags': {
            'type': 'list',
            "elastic" : {    
                "index"  : "not_analyzed"
            }
        },
        'published_from' : { "type": 'date' },
        'lines' : { "type": 'integer' }
    }


    #
    # your model's methods down here
    # (the two below are just examples from the elasticsearch_dsl py documentation)
    #
    def save(self, ** kwargs):
        self.lines = len(self.body.split())
        self.upsert()

    def is_published(self):
        return datetime.now() < self.published_from
