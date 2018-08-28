from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from {{appname}}.powlib import get_class_name
from {{appname}}.config import myapp
from {{appname}}.application import log_handler
import logging

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
#fileConfig(myapp["logfile"])
logging.getLogger('alembic').addHandler(log_handler)
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

#
# this must load all models to give alembic insight
# to the declarative schema
# 
import os
exclude_list=["modelobject", "basemodel", "elastic", "tinydb", "tinymodel", "sqlmodel", "mongomodel"]
#
# the list of modules (excluding _ones and basemodel. Add more you dont want
# to be loaded or inspected to exclude_list above.)
#
mods=[]
module_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'models/sql'))
for mod in os.listdir( module_path ):
    mod = mod.split(".")[0]
    if not mod.startswith("_") and not mod in exclude_list:
        tmp_mod=mod.split("_")[-1]
        # exclude all ending with _observer (which are not models but observers by convention ;)
        if tmp_mod != "observer":
            mods.append(mod)

from sqlalchemy import engine_from_config, pool, MetaData
print(mods)
class_list = []
# load all the models from their modules (mods)
import importlib
for m in mods:
    mod = importlib.import_module('{{appname}}.models.sql.' + m)
    #model_class_name = m.capitalize()
    model_class_name = get_class_name(m)
    klass = getattr(mod, model_class_name)
    class_list.append(getattr(klass, "metadata"))

# alembic support multiple model files 
# see: http://liuhongjiang.github.io/hexotech/2015/10/14/alembic-support-multiple-model-files/
def combine_metadata(*args):
    m = MetaData()
    for metadata in args:
        for t in metadata.tables.values():
            t.tometadata(m)
    return m

# hand over the model class list to combine_metadata
# using lists and *args see: http://stackoverflow.com/questions/28986787/how-to-build-arguments-for-a-python-function-in-a-variable
# ans see: tests/test_args.py
target_metadata = combine_metadata(*class_list)
#from {{appname}}.dblib import Base

#target_metadata = Base.metadata
# orig: target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    print("SQLAlchemy URL: " + str(url))
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
