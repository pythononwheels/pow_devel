    moddir="/../views/mako_modules"
    mylookup = TemplateLookup(directories=[os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)),"../views/") ) ])
    
    
    def __init__(self):
        # define all actions which need alogged in User here
        self.login_required = []
        # define all actions which cannot be called via Http at all here:
        self.locked_actions = []
        
        
    