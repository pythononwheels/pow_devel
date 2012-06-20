import sys, datetime, os, getopt, shutil
import ConfigParser,string
import re

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.normpath("./"))
import powlib


class PowObject(object):
	""" pow base object class"""
	__engine__= None
	__metadata__ = None
	__session__= None
	
	def dump(sql, *multiparams, **params):
	    print sql.compile(dialect=engine.dialect)
	
	def __init__(self):
		PowObject.__engine__= create_engine(powlib.get_db_conn_str())
		PowObject.__metadata__ = MetaData()
		PowObject.__metadata__.bind =  PowObject.__engine__
		PowObject.__metadata__.reflect(PowObject.__engine__)
		PowObject.__session__= sessionmaker()
		PowObject.__session__.configure(bind=PowObject.__engine__)
		
	def dispatch(self):
		print "object:" + str(self) +  "dispatch() method invoked"
		return
		
	def getMetaData(self):
		return PowObject.__metadata__
	
	def getEngine(self):
		return PowObject.__engine__
		
	def getSession(self):
		return PowObject.__session__()
		
	def repr(self):
		return "Not implemented in class: PowObject"