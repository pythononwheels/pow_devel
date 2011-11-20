import sys, datetime, os, getopt, shutil
import ConfigParser,string
import re

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.normpath("./"))
import powlib


class PowAppObject(object):
	""" pow App object class, creates the connection to the app.db"""
	#__engine__= create_engine(powlib.get_db_conn_str("../config/"))
	__engine__= None
	__metadata__ = MetaData(bind = __engine__)
	__session__ = sessionmaker(bind = __engine__)
	
	def __init__(self):
		PowAppObject.__engine__= create_engine(powlib.get_app_db_conn_str())
		#print powlib.get_app_db_conn_str()
		PowAppObject.__metadata__.bind =  PowAppObject.__engine__
		PowAppObject.__session__.configure( bind = PowAppObject.__engine__ )
		
	def dispatch(self):
		print "object:" + str(self) +  "dispatch() method invoked"
		return
		
	def getMetaData(self):
		return PowAppObject.__metadata__
	
	def getEngine(self):
		return PowAppObject.__engine__
	
	def getSession(self):
		return PowAppObject.__session__()
	
	def getConnection(self):
		return PowAppObject.__engine__.connect()
		
	def repr(self):
		return "Not implemented in class: PowAppObject (Except for this print, which is in fact an implementation ;)"
