#
#
# You can enter all changes that should be available to all PoW controllers here.
# Inheritance sequence 
#    Basecontroller->ApplicationController->allOtherControllers
# 
# As an exampole pre_filter and post_filter are implemented here
# 
# date created:     2012-08-10
# khz@pythononwheels.org
#

import sys
import os

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../models" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../models/powmodels" )))

import BaseController
import powlib
import inspect



class ApplicationController(BaseController.BaseController):
    
    def __init__(self):
        """        initialisation        """
        super(ApplicationController,self).__init__()
        self.modelname = "None"
        self.locked_actions = {}
        # Format: { filter: ( selector, [list of actions] ) } 
        self.pre_filter_dict = {}
        
    
    def pre_filter(self, filter, selector ,action_list = []):
        """
        set a pre_filter operation for controller actions.
        @param filter:             Name of the filter to be executed before the action (Module.Class.Method) 
                                     if there are no dots self.filter is assumed
        @param selector:           One of: any, except,only
        @param action_list:        If selector is except OR only, this defines the actions in scope.
        """
        # check if filter already set.
        if not self.pre_filter_dict.has_key(filter):
            # check if selector correct
            if selector in ["any", "except", "only"]:
                # set the filter
                if selector == "any":
                    import inspect
                    alist =  inspect.getmembers(self, predicate=inspect.ismethod)
                    for elem in alist:
                        print elem[0]
                elif selector == "only":
                    for func in action_list:
                        if self.pre_filter_dict.has_key(func):
                            self.pre_filter_dict[func].append(filter)
                        else:
                            self.pre_filter_dict[func] = [filter]
                elif selector == "except":
                    pass
                print "Added pre_filter: ", self.pre_filter_dict
                return True
            else:
                raise NameError("selector must be one of: only, except or any. You gave %s" % (str(selector)))
                return False
        return False
    
    #def __getattribute__(self,name):
    #    # check if pre_filter needs to be applied
    #    if name != '__dict__':
    #        #print '__getattribute__', name
    #        if name in self.__dict__["pre_filter_dict"].keys():
    #            print "filter found"
    #        else:
    #            print "no filter found",  self.__dict__["pre_filter_dict"].keys()
    #            
    #    ret = BaseController.__getattribute__(self,name)
    #    
    #    return ret    
        


    