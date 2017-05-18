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

def pow_init_from_dict_deserializer(dct, schema):
    """
        takes a dict with attributes and values 
        and (tries) to convert them to the specified types given in the schema
        Can be used in model.init_from_dict. (Which most often follows an init_from_json call)
                HTTP Request (data) => init_from_json(data) => dict(data) => init_from_dict(data, schema) => Model
        Reason:
            json data from ajax requests has for example dates as string but you most probably want datetime.
    """
    for elem in dct:
        if elem in schema.keys():
            print("converting: " + str(elem) + " : " + str(dct[elem]) + " => " + schema[elem]["type"] ) 
            if schema[elem]["type"].lower() == "datetime":
                if not isinstance(dct[elem], (datetime.datetime)):
                    try:
                        dct[elem] = datetime.datetime.strptime(dct[elem], myapp["date_format"])
                        print(str(type(dct[elem])) + str(dct[elem]))
                    except Exception as e:
                        raise e
            elif schema[elem]["type"].lower() == "integer":
                if not isinstance(dct[elem], (int)):
                    try:
                        dct[elem] = int(dct[elem])
                    except Exception as e:
                        raise e
            elif schema[elem]["type"].lower() == "boolean":
                if not isinstance(dct[elem], (bool)):
                    try:
                        dct[elem] = bool(dct[elem])
                    except Exception as e:
                        raise e
            elif schema[elem]["type"].lower() == "string":
                if not isinstance(dct[elem], (str)):
                    try:
                        dct[elem] = str(dct[elem])
                    except Exception as e:
                        raise e
            elif schema[elem]["type"].lower() == "list":
                if not isinstance(dct[elem], (list)):
                    try:
                        dct[elem] = list(dct[elem])
                    except Exception as e:
                        raise e
            elif schema[elem]["type"].lower() == "float":
                if not isinstance(dct[elem], (float)):
                    try:
                        dct[elem] = float(dct[elem])
                    except Exception as e:
                        raise e
            elif schema[elem]["type"].lower() == "set":
                if not isinstance(dct[elem], (set)):
                    try:
                        dct[elem] = set(dct[elem])
                    except Exception as e:
                        raise e
    return dct
