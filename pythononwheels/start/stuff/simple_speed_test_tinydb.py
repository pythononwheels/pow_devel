#
# simpletest tinydb
#

from redis2.models.tinydb.testdata import Testdata
import time

start = time.time()
NUM=10000
for x in range(0,NUM):
    t=Testdata()
    #print(t.key)
    #print(t.created_at)
    t.upsert()
end = time.time()

print("inserting {} elements took: {}".format(str(NUM),str(end - start)))