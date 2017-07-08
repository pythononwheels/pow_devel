import tornado.web
import tornado.escape
import json
from {{appname}}.config import myapp 
from {{appname}}.handlers.base import BaseHandler

class PowHandler(BaseHandler):
    """
        The Base PowHandler 
        Place to put common stuff which will remain unaffected by any PoW Changes.
        Purely and only User or Extension controlled.

        Example is authentication.
    """
    show_list=[]
    hide_list=[]
    def get_current_user(self):
        """
            very simple implementation. 
            change to you own needs here or in your own subclassed base handler.

        """
        if myapp["enable_authentication"]:
            # try to find the user
            # user_id = self.get_secure_cookie("user_id")
            # if not user_id: return None
            # u=User()
            # u=u.find_one(User.id==user_id)
            # return u
            raise NotImplementedError("USer Authentication not implemented, yet")
        else:
            # if authentication is disabled return a dummy guest user
            return True
        

    def success(self, **kwargs):
        """ 
            just adding a user object to every success call
        """
        # add your modifications below.
        # add arguements that are needed by all viwes etc ..
        BaseHandler.success(self, **kwargs)