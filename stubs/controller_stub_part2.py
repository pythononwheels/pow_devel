		BaseController.BaseController.__init__(self)
	
	def list( self, powdict ):
		res = self.model.find_all()
		return self.render(model=self.model, powdict=powdict, list=res)
	
	def show( self,powdict ):
		res = self.model.find_by("id",powdict["PARAMETERS"]["id"])
		return self.render(model=self.model, powdict=powdict)
		
	def new( self, powdict ):
		self.model.__init__()
		dict = powdict["PARAMETERS"]
		for key in dict:
			self.model.set(key, dict[key] )
		self.model.create()
		return self.render(model=self.model, powdict=powdict)
	
	def create( self, powdict):
		self.model.__init__()
		return self.render(model=self.model, powdict=powdict)
	
	def edit( self, powdict ):
		res = self.model.find_by("id",powdict["PARAMETERS"]["id"])
		return self.render(model=res, powdict=powdict)
	
	def update( self, powdict ):
		#self.model.__init__()
		self.model = self.model.find_by("id",powdict["PARAMETERS"]["id"])
		dict = powdict["PARAMETERS"]
		for key in dict:
			self.model.set(key, dict[key] )
		self.model.update()
		return self.render(model=self.model, powdict=powdict)
	
	def delete( self, powdict ):
		self.model.__init__()
		self.model = self.model.find_by("id",powdict["PARAMETERS"]["id"])
		self.model.delete(self.model.get_id())
		return self.render(model=self.model, powdict=powdict)
