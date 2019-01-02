import tornado.web
import tornado.escape
import json
import werkzeug.security 
import os
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
        if myapp["enable_auth"]:
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
        method = myapp["pwhash_method"]
        return werkzeug.security.generate_password_hash(password, method=method, salt_length=8)

    def get_post_file(self, form_field_name ):
        """ 
            gets the file info from a POSTed html form.
            param: name of the 
        """
        # [{'filename': 'test.mp3', 'body': b'Nur ein Test', 'content_type': 'audio/mpeg'}]
        file_info = self.request.files['file'][0]
        original_fname = file1['filename']
        fname, extension = os.path.splitext(original_fname)
        file_info["extension"] = extension
        file_info["fname"] = fname
        sec_filename = secure_filename(original_fname)
        file_info["secure_filename"] = sec_filename
        file_info["secure_upload_path"]= os.path.join(myapp["upload_path"],sec_filename )
        return file_info

    def success(self, **kwargs):
        """ 
            just adding a user object to every success call
        """
        # add your modifications below.
        # add arguements that are needed by all viwes etc ..
        BaseHandler.success(self, **kwargs)