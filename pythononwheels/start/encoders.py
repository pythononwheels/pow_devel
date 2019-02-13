#
# encoders for various output formats
# 
# the dumps() method will be called
#
import io
import csv
import dicttoxml
from datetime import datetime
import uuid
import {{appname}}
import simplejson as json

def pow_json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        #serial = obj.isoformat()
        serial = obj.strftime(todo.config.myapp["date_format"])
        return serial
    if isinstance(obj, uuid.UUID):
        return str(obj)
    # add your own additions below here.

    raise TypeError ("Type not serializable")

class json_to_json:
    """
        receives a list of json and returns a string
    """
    def dumps(self, data):
        return json.dumps(data, default=pow_json_serializer) 
        
    

class json_to_csv:
    """ flattens json and converts the flattened
        data to csv
    """
    def flattenjson(self, mp, delim="_"):
        """ flattens a json. 
            separated nested keys are chained using delim
            {
                "a" : {
                    "b" : "1",
                    "c" : "2"
                }
            }
            rsults in =>
            {
                "a_b"   :  "1",
                "a_c"   :  "2",
            }
        """
        ret = []
        if isinstance(mp, dict):
            for k in mp.keys():
                csvs = self.flattenjson(mp[k], delim)
                for csv in csvs:
                    ret.append(k + delim + str(csv))
        elif isinstance(mp, list):
            for k in mp:
                csvs = self.flattenjson(k, delim)
                for csv in csvs:
                    ret.append(str(csv))
        else:
                ret.append(mp)

        return ret
    
    def dumps(self, data):
        """ dumps data to csv.
            data will be flattened before
        """
        output = io.StringIO()
        #writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer = csv.DictWriter(output, data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

class json_to_xml:
    def dumps(self, data, root="pow_model"):
        """ 
            returns the xml representation of a dict input data
            root / custom_root is the root node name of the xml document.

            data is a dict.

            usage: encoder.dumps(model.to_dict, root="some custom root name")
        """
        print(data)
        #print(dicttoxml.dicttoxml(data))
        if not isinstance(data, list):
            try:
                res = list(data)
            except:
                return dicttoxml.dicttoxml(str(data), custom_root=root)
        
        try:
            reslist =  [str(dicttoxml.dicttoxml(x, custom_root=root)) for x in data]
            
        except Exception as e:
            print("ERRRR  : " + str(e))
        if len(reslist) == 1:
            return reslist[0]
        else:
            return "".join(reslist)
        #return dicttoxml.dicttoxml(data, custom_root=root)