import os,sys
import time,datetime
from sqlalchemy import Column
from sqlalchemy.orm import mapper
from sqlalchemy import Table

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" )))
import powlib
from PowObject import PowObject

class BaseMigration(PowObject):
	table_name = "None"
	# self.table is set to a PowTable Object in the migration
	table = None
	
	def __init__(self):
		PowObject.__init__(self)

	def create_table(self):
		if self.table != None:
			self.table.create(bind=PowObject.__engine__, checkfirst=True)
		else:
			raise StandardError("Pow ERROR: table was None")
		
	def drop_table(self, model = None):
		try:
			if model == None:
				self.table = Table(self.table_name, PowObject.__metadata__, autoload = True )
			else:
				self.table = model.__table__
			if self.table != None:
				self.table.drop(bind=PowObject.__engine__, checkfirst=True)
		except:
			raise StandardError("Pow ERROR: table does not exist")