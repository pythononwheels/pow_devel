from testapp.models.elastic.testelastic import Testelastic
from datetime import datetime

# create the mappings in elasticsearch
Testelastic.init()

# create and save and article
article = Testelastic(meta={'id': 42}, title='Hello world!', tags=['test'])
article.body = ''' looong text '''
article.published_from = datetime.now()
article.save()

article = Testelastic.get(id=42)
print(article.is_published())

# Display cluster health
print(connections.get_connection().cluster.health())