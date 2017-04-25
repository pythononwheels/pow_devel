#
# elastic playground
#

# make sure ES is up and running
import requests
res = requests.get('http://localhost:9200')
print(res.content)