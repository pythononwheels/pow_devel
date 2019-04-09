#
# base connection for sql DBs
#
from {{appname}}.config import database, myapp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import logging

db_log_file_name = myapp["logfile"]
db_handler_log_level = database["sql"]["loglevel"]
db_logger_log_level = database["sql"]["loglevel"]

formatter = myapp["logformat"]

db_handler = logging.FileHandler(db_log_file_name)
db_handler.setLevel(db_handler_log_level)
db_handler.setFormatter(formatter)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_logger_log_level)


sqldb = database["sql"]
conn_str = sqldb["type"] + "://" 
if sqldb["user"]:
    conn_str += sqldb["user"] 
if sqldb["passwd"]:
    conn_str += ":" + sqldb["passwd"] 
if sqldb["host"]:
    conn_str += "@" +sqldb["host"] 
if sqldb["port"]:
    conn_str += ":" +str(sqldb["port"]) 
if sqldb["dbname"]:
    conn_str += "/" + sqldb["dbname"]

engine = create_engine(conn_str, echo=False)
metadata = MetaData(engine)

Session = sessionmaker(bind=engine)

#Transaction = Session   # see:

session = Session()
transaction = session

# for transcations you can use either
# session.begin_nested() or session.begin()  (see below)
# OR transcation.begin_nested() or transaction.begin()  (see below)
# more:
#  http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html


# easiest way to use transactions is:
# session.add(u1)
# session.add(u2)

# session.begin_nested() # establish a savepoint
# session.add(u3)
# session.rollback()  # rolls back u3, keeps u1 and u2

# session.commit() # commits u1 and u2

from sqlalchemy.ext.declarative import declarative_base
#from {{appname}}.models.sql.basemodel import SqlBaseModel
from {{appname}}.models.sql.sqlmodel import SqlModel
Base = declarative_base(cls=SqlModel, metadata=metadata)
Base.metadata.bind = engine

