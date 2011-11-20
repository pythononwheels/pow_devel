
	def __init__(self):
		self.session = self.pbo.getSession()
		self.generate_accessor_methods()
		self.t = self.__table__
		self.setup_properties()
	
	def setup_properties(self):
		for elem in self.properties_list:
			modelname = string.capitalize(powlib.singularize(elem))
			rel_model = powlib.load_class(modelname, modelname)
			self.__mapper__.add_properties({ elem : relationship(rel_model.__mapper__) })
		
	def find_by(self, att, val, first=True):
		mstr = "self.session.query(Base" + self.__class__.__name__ +").filter_by(" + str(att) + "=val)"
		if first == True:
			mstr += ".first()"
		print mstr
		res= eval(mstr)
		#res.__init__()
		return res

	def find_all(self):
		mstr = "self.session.query(Base" + self.__class__.__name__ + ").all()"
		print mstr
		res= eval(mstr)
		#for elem in res:
		#	elem.__init__()
		return res

	def get(self, name):
		return eval("self.get_"+ str(name)+"()")

	def set(self,name,val):
		#eval("self.set_"+ str(name)+"("+val + ")" )
		eval("self.set_"+ str(name)+"(\""+str(val) + "\")" )

	def getColumns(self):
		rlist = []
		for col in self.__table__.columns:
			rlist.append( string.split(str(col), ".")[1])
		return rlist

	def getColumn(self, name):
		return eval("self.__table__.c." + name)

	def getName(self):
		return self.__class__.__name__

	def generate_accessor_methods(self):
		#
		# generates the convenient getAttribute() and setAttribute Methods
		# and sets them as accessors for the variable
		mstr = ""
		self.has_accessor_methods = True
		for item in self.__table__.columns:
			#getter
			mstr = ""
			method_name = "get_"+ item.name
			setter = method_name
			tmp_meth_name = "foo"
			mstr +=	 "def foo(self):" + powlib.newline
			mstr += powlib.tab + "return self." + str(item.name) + powlib.newline
			#print mstr
			exec(mstr)
			self.__dict__[method_name] = types.MethodType(foo,self)
			
			
			# setter
			mstr = ""
			method_name = "set_"+ item.name
			getter = method_name
			tmp_meth_name = "foo"
			mstr +=	 "def foo(self, value):" + powlib.newline
			mstr += powlib.tab + "self." + str(item.name) + " = value " + powlib.newline
			#print mstr
			exec(mstr)
			self.__dict__[method_name] = types.MethodType(foo,self)
			
			cmd_str = "self.__table__." + item + "=property(" + getter + "," + setter + ")"
			eval(cmd_str)
			
	def generate_find_by( self ):
		pass

	def get_by(self, name):
		return eval("self." + str(name))


	def __repr__(self):
		ostr=""
		ostr += str(type(self)) + powlib.newline
		ostr += "-------------------------------" + powlib.newline
		for col in self.__table__.columns:
			ostr += col.name + "-->" + str(self.get_by(col.name)) + powlib.newline
		return ostr

	def __reprhtml__(self):
		ostr=""
		ostr += str(type(self)) + "<br>"
		ostr += "<hr>"
		for col in self.__table__.columns:
			ostr += col.name + "-->" + str(self.get_by(col.name)) + "<br>"
		return ostr

	def update(self):
		dt = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
		self.set("last_updated", dt)
		self.session.merge(self)
		self.session.commit()

	def create(self):
		dt = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
		self.set("created", dt)
		self.set("last_updated", dt)
		self.session.merge(self)
		self.session.commit()

	def delete(self, id):
		s = delete(self.__table__, self.__table__.columns.id==id)
		self.session.execute(s)
		self.session.commit()

	@orm.reconstructor
	def init_on_load(self):
		if self.session == None:
			self.session = self.pbo.getSession()
		if self.has_accessor_methods == False:
			self.generate_accessor_methods()

	def belongs_to(self,rel_table):
		#
		# Now creating the foreign_key
		#
		fkey = powlib.pluralize(rel_table) + ".id"
		if fkey in self.__table__.foreign_keys:
			err_msg = " already has a belongs_to relation to table "
			print "Table ", self.__table__.name, err_msg , rel_table
			raise StandardError( "Table " + self.__table__.name +  err_msg +  rel_table)
		else:
			fkey = ""
			#cons = ForeignKeyConstraint([table.c.fkey], [othertable.c.id])
			modelname = string.capitalize(rel_table)
			#print " -- loading model: ", modelname
			rel_model = powlib.load_class(modelname, modelname)
			#col = rel_model.getColumn(self.__table__.name + "_id")
			#print rel_model.getColumns()
			#print str(CreateTable(rel_model.__table__))
			self.__table__.append_column(Column(rel_model.__table__.name + "_id", Integer, ForeignKey(rel_model.__table__.name +".id")))
			cts = str(CreateTable(self.__table__))
			create_table_ddl = DDL(cts)	
			print cts
			self.__table__.drop()
			self.pbo.getConnection().execute(create_table_ddl)
		return

	def release_belongs_to(self,rel_table):
		return

	def release_has_many(self,rel_table):
		if rel_table in self.properties_list:
			# remove raltion from the living model
			self.properties_list.remove(rel_table)
			print "properties_list after release_has_many:" , self.properties_list 
			mod = powlib.load_module( "generate_model" )
			# daclaration of render_model: def render_model(modelname, force, comment, properties=None, nomig=False):
			# remove relation from the persistent model
			mod.render_model( str.lower(self.modelname), True, "", str(self.properties_list), True)
		else:
			print "Model: ", self.modelname, " has no has_many relation to ", rel_table
		return


	def has_many(self,rel_table):
		### has_many property is the plural form of the modelname
		#modelname = string.capitalize(powlib.singularize(rel_table))
		#rel_model = powlib.load_class(modelname, modelname)
		#self.__mapper__.add_properties({rel_table: relationship(rel_model.__mapper__)})
		#generate_model.render_model(modelname, noforce, comment, properties=None):
		#return
		if rel_table in self.properties_list:
			print "Model: ", self.modelname, " already has a has_many relation to ", rel_table
			return
		else:
			self.properties_list.append(rel_table)
			mod = powlib.load_module( "generate_model" )
			# daclaration of render_model: def render_model(modelname, force, comment, properties=None, nomig=False):
			mod.render_model( str.lower(self.modelname), True, "", str(self.properties_list), True)
			return
		
if __name__ == "__main__":
	pass