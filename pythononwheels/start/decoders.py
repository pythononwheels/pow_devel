import datetime
from {{appname}}.config import myapp
import re

def pow_json_deserializer(dct):
        """
            converting json date stings to datetime.datetime for created_at and last_updated
            see: https://docs.python.org/3/library/json.html
            and: http://stackoverflow.com/questions/8793448/how-to-convert-to-a-python-datetime-object-with-json-loads
                    Nicola of course ;)
        """
        
        if "created_at" in dct:
            print("json deserializer found: created at: " + str(dct["created_at"]))
            #dct["created_at"]=datetime.datetime.strptime(dct["created_at"], myapp["date_format"])
        
        
        return dct