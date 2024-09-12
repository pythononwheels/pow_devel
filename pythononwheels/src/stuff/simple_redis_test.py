
#
# simple redis test
#
from models.redis.todo import Todo
t=Todo()
t.title="new new new"
print( "t: {}".format(t.to_dict()) )
t.key="todo:"+t._uuid
print(t.key)
print(t.to_json())
r=t.upsert()
print(r)
print("fetch from db: key: {} -> {}".format(t.key, t.db.get(t.key)))
t1=Todo()
t1.init_from_json(t.db.get(t.key))
print(t1)
t.db.keys()
print(40*"=")
print(" starting speedtest....")
print(40*"=")
import time
start = time.time()
for elem in range(0,10000):
    t=Todo()
    t.key="todo:"+t._uuid
    t.title="new todo number: " + str(elem)
    t.upsert()
end = time.time()
print("inserting 10000 elements took: {}".format(str(end - start)))