    
import tornado.web
import werkzeug.security 
import {{appname}}.conf.config as cfg

class PowHandlerMixin():
    """
        The Base Pow Handler Mixin Handler 
        This is Place to put common stuff for all your 
        Standard AND WebSocket handlers which will remain unaffected by any PoW Changes.
        Purely and only User or Extension controlled.
    """
    
    show_list=[]
    hide_list=[]
    def get_current_user(self):
        """
            very simple implementation. 
            change to you own needs here or in your own subclassed base handler.

        """
        if cfg.myapp["enable_auth"]:
            # Implement some authentication and authorisation code
            # default implementation will raise the not implemented error.
            raise NotImplementedError("User Authentication not implemented, yet")
        else:
            # if authentication is disabled return a dummy guest user
            return True
        
    def check_password_hash(self, pwhash, password ):
        """
            uses werkzeug.security.check_password_hash
            see: http://werkzeug.pocoo.org/docs/0.14/utils/#module-werkzeug.security
            get the password from for example a login form (make sure you use https)
            get the hash from the user model table (see generate_password_hash below)
        """
        return werkzeug.security.check_password_hash(pwhash, password)

    def generate_password_hash(self, password ):
        """
            uses werkzeug.security.generate_password_hash 
            see: http://werkzeug.pocoo.org/docs/0.14/utils/#module-werkzeug.security
            store this returned hash in the user models table as password
            when the user is first registered or changed his password.
            Use https to secure the plaintext POSTed pwd.
        """
        method = cfg.myapp["pwhash_method"]
        return werkzeug.security.generate_password_hash(password, method=method, salt_length=8)