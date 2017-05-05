#
# update-db
#
import os
import alembic.config
import sys
from {{appname}}.database.sqldblib import engine
from alembic.config import Config
from alembic import command
import argparse
import logging
import warnings
from sqlalchemy import exc as sa_exc
#
# this will execute 
# alembic upgrade head
# where message is the first cli parameter
#


# see here: http://alembic.zzzcomputing.com/en/latest/api/commands.html
def migrate(direction, revision=None, number=1, path=None):

    #
    # really migrate
    #
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        if path:
            alembic_cfg = Config(os.path.join(path, "alembic.ini"))
        else:
            alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
        if direction == "up":
            # upgrade
            if revision:
                res = command.upgrade(alembic_cfg, revision=revision)
            if number == "head":
                res = command.upgrade(alembic_cfg, "head")
            else:
                res = command.upgrade(alembic_cfg, "+" + str(number))
        elif direction == "down":
            # downgrade
            res = command.downgrade(alembic_cfg, "-" + str(number))
    
    return res

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--direction", action="store", default=None,
        dest="direction", help='-d up (or down) default = up',
        required=False)
    #
    # db type
    # 
    parser.add_argument('-n', "--number", action="store",
        dest="number", help='-n 1 (default = 1)',
        default="1", required=False)

    parser.add_argument('-r', "--revision", action="store",
        dest="revision", help='-r 6669c0b62b06 (take the unique part from a migration id)',
        default=None, required=False)
    
    parser.add_argument('-c', "--current", action="store_true",
        dest="current", help='Display the current revision for a database.',
        default=False, required=False)

    parser.add_argument('-l', "--list", action="store_true",
        dest="history", help='List changeset scripts in chronological order.',
        default=False, required=False)

    args = parser.parse_args()
    #
    # show some args
    #
    #print("all args: ", args)

    

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)

        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
        
        # show the current version
        if args.current:
            print(50*"-")
            print("current version: ")
            print(50*"-")
            command.current(alembic_cfg, verbose=True)
            sys.exit()

        # show all changes
        if args.history:
            print(50*"-")
            print("revision history: ")
            print(50*"-")
            command.history(alembic_cfg, rev_range=None, verbose=False)
            sys.exit()
        

        #
        # really migrate
        #
        res = "NOTHING"
        if args.direction == "up":
            # upgrade
            res = migrate("up", args.revision, args.number)
        elif args.direction == "down":
            # downgrade
            res = migrate("down", args.revision, args.number)
        else:
            print("Error: ")
            print("You must at least give a direction info up / down to migrate:")
            print(50*"-")
            print(" Change history ")
            print(50*"-")
            command.history(alembic_cfg, rev_range=None, verbose=False)
        #print(" res type: " + str(type(res)))
        #print(str(res))
        #print(" res dir: " + str(dir(res)))
        sys.exit()

if __name__ == "__main__":
    main()