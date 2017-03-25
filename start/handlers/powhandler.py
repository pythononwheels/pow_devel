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

    def get_current_user(self):
        """
            very simple implementation. 
            change to you own needs here or in your own subclassed base handler.

        """
        if myapp["enable_authentication"]:
            # try to find the user
            user_id = self.get_secure_cookie("user_id")
            if not user_id: return None
            u=User()
            u=u.find_one(User.id==user_id)
            return u
        else:
            # if authentication is disabled return a dummy guest user
            u=User()
            u.login="pow_guest"
            return None