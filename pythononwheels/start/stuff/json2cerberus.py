#
# test to convert json data to 
# a cerberus schema.
# Cerberus types see here: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
#
# sampledata: https://www.json-generator.com/

import simplejson as json
import re
from dateutil.parser import parse

uuid = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)

def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    cerberus_schema = {}
    # sample output schema format:
    # schema = {'name': {'type': 'string'} }

    f = open("sampledata.json","r")
    # already covers bool, list, dict
    data = json.load(f)
    #print(data)
    for elem in data[0]:
        #print("{0} : {2} : {1}".format(elem, str(type(data[0][elem])), str(data[0][elem])), end='')
        current_element=data[0][elem]
        if isinstance(current_element, bool):
            cerberus_schema[elem] = {"type" : "boolean" }
        elif isinstance(current_element, int):
            cerberus_schema[elem] = {"type" : "integer" }
        elif isinstance(current_element, float):
            cerberus_schema[elem] = {"type" : "float" }
        elif isinstance(current_element, list):
            cerberus_schema[elem] = {"type" : "list" }
        elif isinstance(current_element, dict):
            cerberus_schema[elem] = {"type" : "dictionary" }
        elif isinstance(current_element, str):
            # date and datetime (date = datetime with constantly missing h:m:s)
            if is_date(data[0][elem]):
                cerberus_schema[elem] = {"type" : "datetime" }
                #print(" AND string is => date or datetime")
            else:
                cerberus_schema[elem] = {"type" : "string" }
                #print()
        elif isinstance(current_element, bytes) or isinstance(current_element, bytearray):
            cerberus_schema[elem] = {"type" : "binary" }
            #print(" AND binary")
        else:
            print()
    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=4)
    pp.pprint(cerberus_schema)