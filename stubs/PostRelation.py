
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm
from sqlalchemy.sql import delete

import sys,os
import string
import types

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" ))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./basemodels" ))
import powlib
from PowBaseObject import PowBaseObject
import PostRelation

x = PowBaseObject()

Base = declarative_base(bind=x.__engine__, metadata = x.__metadata__)
Base.metadata.reflect()

class PostRelation():
	#
	# Class: PostRelation
	#
	def relation(self, rel):	
		pass
		
if __name__ == "__main__":
	pass
	