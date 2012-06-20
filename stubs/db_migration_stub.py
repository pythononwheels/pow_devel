from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Sequence

metadata = MetaData()

# below you see an example on how to create the model data

users_table = Table('users', metadata,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('name', String(50)),
    Column('fullname', String(50)),
    Column('password', String(12))
)

