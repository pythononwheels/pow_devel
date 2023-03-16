import tornado.web
import tornado.escape
import json
import werkzeug.security 
import os
from {{appname}}.conf.config import myapp 
from {{appname}}.handlers.base import BaseHandler
from {{appname}}.handlers.powhandlermixin import PowHandlerMixin

class PowHandler(PowHandlerMixin, BaseHandler):
    """
        The Base PowHandler 
        Place to put common stuff which will remain unaffected by any PoW Changes.
        Purely and only User or Extension controlled.

        Example is authentication.
    """
   

    def get_post_file(self, body=False, form_field_name="file" ):
        """ 
            gets the file info from a POSTed html form.
            param: name of the form field where the file is added

            #todo: take the binary data from the posted body directly.
             => but then additional info like filename and extension are missing.
             
        """
        # [{'filename': 'test.mp3', 'body': b'Nur ein Test', 'content_type': 'audio/mpeg'}]
        file_info = {}

        file1 = self.request.files[form_field_name][0]
        original_fname = file1['filename']
        fname, extension = os.path.splitext(original_fname)
        file_info["fname_full"] = original_fname
        file_info["extension"] = extension
        file_info["fname"] = fname
        secure_filename = werkzeug.utils.secure_filename(original_fname)
        file_info["secure_filename"] = secure_filename
        file_info["secure_upload_path"]= os.path.join(myapp["upload_path"],secure_filename )
        with open( file_info["secure_upload_path"], 'wb') as output_file:
            output_file.write(file1['body'])
        return file_info

    def success(self, **kwargs):
        """ 
            just adding a user object to every success call
        """
        # add your modifications below.
        # add arguements that are needed by all viwes etc ..
        BaseHandler.success(self, **kwargs)