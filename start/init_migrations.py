#
# adapts the alembic migrations ini
# to changes in the pow db config
#
from {{appname}}.database.sqldblib import conn_str
import configparser

def init_migrations(stdout=False):
    #config= configparser.ConfigParser.RawConfigParser()
    config= configparser.ConfigParser()
    config.read(r'alembic.ini')
    config.set('alembic','sqlalchemy.url',conn_str)
    with open(r'alembic.ini', 'w') as configfile:
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