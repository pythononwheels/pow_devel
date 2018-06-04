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
    f = open("sampledata.json","r")
    data = json.load(f)
    #print(data)
    for elem in data[0]:
        print("{0} : {2} : {1}".format(elem, str(type(data[0][elem])), str(data[0][elem])), end='')
        if isinstance(data[0][elem], str):
            # check for uuid
            if uuid.match(data[0][elem]):
                print(" AND string is => uuid")
            elif is_date(data[0][elem]):
                print(" AND string is => date or datetime")
            else:
                print()
        else:
            print()