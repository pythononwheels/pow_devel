#
# test to convert json data to 
# a cerberus schema.
# Cerberus types see here: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
#
# sampledata: https://www.json-generator.com/
#
# this uses the first data element in a given json file to create
# a model(cerberus) schema from it. Trying to guess the right types (without too much effort)
#

import simplejson as json
import re
from dateutil.parser import parse
import sys

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
    if len(sys.argv) < 2:
        print("usage: python json2cerberus.py jsondata.json <optional_start_element>")
        sys.exit()
    infile=sys.argv[1]
    print("opening json data file: {}".format(infile))
    f = open(infile,"r")
    # already covers bool, list, dict
    try:
        raw_data=f.read()
        raw_data=raw_data
        data = json.loads(raw_data)
        #print(dir(data))
        #print(type(data))
        #print(type(data[0]))
    except Exception as e:
        print(e)
    #print(data)
    startelement = None
    if len(sys.argv) == 3:
        startelement = sys.argv[2]
    if startelement:
        mydata=data[startelement][0]
    else:
        mydata=data[0]
    #print(mydata)
    #print(type(mydata))
    for elem in mydata:
        #print("{0} : {2} : {1}".format(elem, str(type(elem)), str(elem), end=''))
        print("Checking Elem: {}".format(elem))
    
        if isinstance(mydata[elem], bool):
            cerberus_schema[elem] = {"type" : "boolean" }
        elif isinstance(mydata[elem], int):
            cerberus_schema[elem] = {"type" : "integer" }
        elif isinstance(mydata[elem], float):
            cerberus_schema[elem] = {"type" : "float" }
        elif isinstance(mydata[elem], list):
            cerberus_schema[elem] = {"type" : "list" }
        elif isinstance(mydata[elem], dict):
            cerberus_schema[elem] = {"type" : "dictionary" }
        elif isinstance(mydata[elem], str):
            # date and datetime (date = datetime with constantly missing h:m:s)
            if is_date(elem):
                cerberus_schema[elem] = {"type" : "datetime" }
                #print(" AND string is => date or datetime")
            else:
                cerberus_schema[elem] = {"type" : "string" }
                #print()
        elif isinstance(mydata[elem], bytes) or isinstance(mydata[elem], bytearray):
            cerberus_schema[elem] = {"type" : "binary" }
            #print(" AND binary")
        else:
            cerberus_schema[elem] = {"type" : "string" }
            print("type unknown, setting string.")
    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=4)
    print(70*"-")
    print("|   find model schema for: {}".format(infile) )
    print(70*"-")
    print("schema=", end="")
    pp.pprint(cerberus_schema)
    print(70*"-")
    print("|   you can copy&paste this right into any PythonOnWheels model schema"  )
    print(70*"-")
    