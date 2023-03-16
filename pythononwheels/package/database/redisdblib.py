#
# base connection for Redis 
#
import {{appname}}.conf.config as cfg
import redis
from powlib import Dbinfo


def generate_connection(redis_conf=None):
    if not redis_conf:
        redis_conf= cfg.database.get("redis", None)
    conn_str = " host:{}, port:{}".format(redis_conf["host"], redis_conf["port"])
    try:
        if redis_conf["strict"]:
            redisdb = redis.StrictRedis(
                    host=redis_conf["host"], 
                    port=redis_conf["port"], 
                    password=redis_conf["passwd"], 
                    db=redis_conf["dbname"],
                    decode_responses=True,
                    socket_connect_timeout=5
                )
        else:
            redisdb = redis.Redis(
                    host=redis_conf["host"], 
                    port=redis_conf["port"], 
                    password=redis_conf["passwd"], 
                    db=redis_conf["dbname"],
                    decode_responses=True,
                    socket_connect_timeout=5
                )
        #print(" ... setting it up for RedisDB: " + conn_str )
        #print(f"redis ping... {redisdb.ping()}")
        return Dbinfo(db=redisdb, collection=None)
    except Exception as e:
        print(f" Exception: {str(e)}")
        raise Exception("I had a problem setting up RedisDB")
