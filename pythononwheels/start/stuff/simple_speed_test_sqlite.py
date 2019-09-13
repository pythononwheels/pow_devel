#
# simpletest sqlite
#

from redis2.models.sql.testdata import Testdata
import time


NUM=100000
olist=[]
for x in range(0,NUM):
    t=Testdata()
    #print(t.key)
    #print(t.created_at)
    olist.append(t)
start = time.time()
# for elem in olist:
#     elem.session.add(elem)
#     elem.session.commit()

t.session.bulk_save_objects(olist)
t.session.commit()
end = time.time()

print("inserting {} elements took: {}".format(str(NUM),str(end - start)))