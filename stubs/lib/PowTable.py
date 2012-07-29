import os,sys
import time,datetime
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.orm import mapper
from sqlalchemy import Text, Sequence, Integer
import datetime
import string

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" )))
import powlib
from PowObject import PowObject

class PowTable(sqlalchemy.Table):
    
    def has_many(self, tablename):
        pass
    
    def belongs_to(self, tablename):
        pass
    
    def many_to_many(self, tablename):
        pass
    
    def append_column_to_db(self, column):
        print dir(column)
        estr = "self.c." + column.name + ".create()"
        print estr
        eval( estr )
    
    def alter_column_name(self, colname, newname):
         eval("self.c." + colname + ".alter(name=\"" + newname + "\")")
         
    def create(self, **kwargs):
        col = Column('created', Text, default=datetime.datetime.now())
        self.append_column( col )
        col = Column('last_updated', Text, default=datetime.datetime.now())
        self.append_column( col )
        col = Column('id', Integer, Sequence(self.name+'_id_seq'), primary_key=True)
        self.append_column( col )
        for elem in self.columns:
            elem.name = string.lower(elem.name)
        sqlalchemy.Table.create(self, **kwargs)
        
    def drop(self, **kwargs):
        sqlalchemy.Table.drop(self, **kwargs)