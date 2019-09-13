#
# simpletest redis
#

from redis2.models.redis.testdata import Testdata
import time
olist=[]
NUM=100000
print("preparing {} objects...".format(str(NUM)))
for x in range(0,NUM):
    t=Testdata()
    olist.append(t)
#     #print(t.key)
#     #print(t.created_at)
#     t.upsert()
# end = time.time()
print("start insert...")
start = time.time()
t.bulk_upsert(olist)

end = time.time()
print("inserting {} elements took: {}".format(str(NUM), str(end - start)))