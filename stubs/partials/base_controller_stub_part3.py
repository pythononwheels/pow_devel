        self.session = self.model.pbo.getSession()
    
    def index(self):
        render()
        
    def render(self, **kwargs):
        if self.check_access(**kwargs) == True:
            fname = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../views/") + self.modelname + "_" + self.current_action +".tmpl")
            mytemplate = Template(filename=fname, lookup=self.mylookup)
            return mytemplate.render(**kwargs)
        else:
            self.setCurrentAction("login")
            fname = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../views/") + self.modelname + "_" + self.current_action +".tmpl")
            mytemplate = Template(filename=fname, lookup=self.mylookup)
            return mytemplate.render(**kwargs)
    
    def setCurrentAction(self, action ):
        self.current_action = action
    
    def redirect(self, action, **kwargs):
        self.setCurrentAction(action)
        return eval("self." + action + "(**kwargs)")
    
    def check_access(self,**kwargs):
        powdict = kwargs.get("powdict",None)
        session = powdict["SESSION"]
        is_logged_in = False
        if self.current_action in self.no_login_required:
            # no login required
            return True
        else:
            # login required
            try:
                if session["user.id"]:
                    return True
            except KeyError:
                    return False
        # by default return False
        return False