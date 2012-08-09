        BaseController.BaseController.__init__(self)
        self.login_required = []
        # put the actions you implemented but do not want to be callable via web request 
        # into the locked_actions dictionary. Format: "actionname" : "redirect_to" }
        # simple_server and pow_router will not call locked actions but redirect to the given value, instead
        self.locked_actions = {}
    
    def list( self, powdict ):
        res = self.model.find_all()
        return self.render(model=self.model, powdict=powdict, list=res)
    
    def show( self,powdict ):
        res = self.model.find_by("id",powdict["REQ_PARAMETERS"]["id"])
        return self.render(model=res, powdict=powdict)
        
    def new( self, powdict ):
        self.model.__init__()
        #print powdict["REQ_PARAMETERS"]
        #print self.model
        dict = powdict["REQ_PARAMETERS"]
        for key in dict:
            statement = 'type(self.model.__table__.columns["%s"].type)' % (key)
            curr_type = eval(statement)
            if curr_type == type(sqlalchemy.types.BLOB()) or curr_type == type(sqlalchemy.types.BINARY()):
                ofiledir  = os.path.normpath("./public/img/")
                print "key: ", key
                if pow_web_lib.get_form_binary_data( key, dict, ofiledir):
                    # if form contains file data AND file could be written, update model
                    self.model.set(key, dict[key].filename )   
                else:
                    # dont update model
                    print " ##### -_______>>>>>>>   BINARY DATA but couldnt update model"
            else:
                self.model.set(key, dict[key])
        
        self.model.create()
        powdict["FLASHTEXT"] ="Yep, record successfully created."
        powdict["FLASHTYPE"] ="success"
        
        return self.render(model=self.model, powdict=powdict)
    
    def create( self, powdict):
        self.model.__init__()
        return self.render(model=self.model, powdict=powdict)
    
    def edit( self, powdict ):
        res = self.model.find_by("id",powdict["REQ_PARAMETERS"]["id"])
        return self.render(model=res, powdict=powdict)
    
    def update( self, powdict ):
        self.model.__init__()
        #print powdict["REQ_PARAMETERS"]
        self.model = self.model.find_by("id",powdict["REQ_PARAMETERS"]["id"])
        #print self.model
        dict = powdict["REQ_PARAMETERS"]
        for key in dict:
            statement = 'type(self.model.__table__.columns["%s"].type)' % (key)
            curr_type = eval(statement)
            if curr_type == type(sqlalchemy.types.BLOB()) or curr_type == type(sqlalchemy.types.BINARY()):
                ofiledir  = os.path.normpath("./public/img/")
                print "key: ", key
                if pow_web_lib.get_form_binary_data( key, dict, ofiledir):
                    # if form contains file data AND file could be written, update model
                    self.model.set(key, dict[key].filename )   
                else:
                    # dont update model
                    print " ##### -_______>>>>>>>   BINARY DATA but couldnt update model"
            else:
                self.model.set(key, dict[key])
        self.model.update()
        return self.render(model=self.model, powdict=powdict)
    
    def delete( self, powdict ):
        self.model.__init__()
        self.model = self.model.find_by("id",powdict["REQ_PARAMETERS"]["id"])
        self.model.delete(self.model.get_id())
        powdict["FLASHTEXT"] ="Yep, record successfully deleted."
        powdict["FLASHTYPE"] ="success"
        return self.render(model=self.model, powdict=powdict)
