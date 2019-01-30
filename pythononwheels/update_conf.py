#
# config for PythonOnWheels 
#   generate_app script
# khz 01/2019

#
# these files and directories are excluded from overrides when using the --update switch
# 
update_conf = {
    "update_exclude_files"  : [ "alembic.ini", "db.sqlite", "tiny.db",
                                "env.py", "shorties.py", "config.py", "powhandler.py", 
                                "powmodel.py", "tinymodel.py", "mongomodel.py" ],
    "update_exclude_dirs"   : [ "migrations",  "static" ]
}