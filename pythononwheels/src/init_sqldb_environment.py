#
# adapts the alembic migrations ini
# to changes in the pow db config
#
from {{appname}}.database.sqldblib import conn_str
import configparser
from {{appname}}.conf.config import database

def init_migrations(stdout=False):
    #config= configparser.ConfigParser.RawConfigParser()
    config= configparser.ConfigParser()    
    config.read(database["sql"]["alembic.ini"])
    config.set('alembic','sqlalchemy.url',conn_str)
    with open(database["sql"]["alembic.ini"], 'w') as configfile:
        config.write(configfile)
    if stdout:
        print(70*"-")
        print("updated migration environment: " + conn_str)
        print(70*"-")
    return True

def main():
    init_migrations(stdout=True)

if __name__=="__main__":
    main()