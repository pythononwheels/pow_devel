#
# generate_migration
#
import os
import alembic.config
import sys
from {{appname}}.database.sqldblib import engine
from alembic.config import Config
from alembic import command
import argparse

#
# this will execute 
# alembic revision --autogenerate -m "message"
# where message is the first cli parameter
#
def generate_migration(message="NONE"):
    import warnings
    from sqlalchemy import exc as sa_exc

    print(40*"-")
    print(" generating migration: " + message)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
    
        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
        script =command.revision(alembic_cfg, autogenerate=True, message=message)
    #print("... " + str(dir(script)) + " done")
    print(" rev: " +str(script.revision))
    print(" path: " +str(script.path))
    
    print(40*"-")

    return script


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", action="store",
        dest="message", help='-n my_first_migration',
        default=None, required=True)

    args = parser.parse_args()
    if args.message:
        generate_migration(message=args.message)    
    else:
        print("You must give a migration name. -n <something>")

if __name__ == "__main__":
    main()