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
# khz 2018
# update: 18.3.2019: nicer schema output.


import simplejson as json
import re
from dateutil.parser import parse
import sys
import click

uuid = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)

def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False

@click.command()
@click.option('--infile', help='json file to read')
@click.option('--usepprint', default=False, is_flag=True, help='use generic pprint to print schema. ')
@click.option('--start_element', default=0, help="Element to process, if json file contains a list. Default=0")
def json_to_cerberus(infile, start_element, usepprint):
    cerberus_schema = {}
    # sample output schema format:
    # schema = {'name': {'type': 'string'} }
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
    mydata=data[start_element]
    #print(mydata)
    #print(type(mydata))
    for elem in mydata:
        #print("{0} : {2} : {1}".format(elem, str(type(elem)), str(elem), end=''))
        #print("Checking Elem: {}".format(elem))

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
            # check if sring is a date format...
            if is_date(mydata[elem]):
                cerberus_schema[elem] = {"type" : "datetime" }
                #print(" AND string is => date or datetime")
                # todo check if it is a dat (date = datetime without h:m:s:.xx)
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
    print("  Model schema for: {}".format(infile) )
    print(70*"-")
    if usepprint:
        print("schema=", end="")
        pp.pprint(cerberus_schema)
        print(70*"-")
    else:
        print("schema={")
        for index,(key,val) in enumerate(cerberus_schema.items()):
            if index < len(cerberus_schema.keys())-1:
                print( "        {0:<25s} : {1:<50s}".format("'"+key+"'",str(val)+","))
            else:
                print( "        {0:<25s} : {1:<50s}".format("'"+key+"'",str(val)))
            #print(" {}  {} {}".format(str(index), key, val))
        print("        }")
    print(70*"-")
    print("   you can copy&paste this right into any PythonOnWheels model schema"  )
    print(70*"-")

if __name__ == "__main__":
    json_to_cerberus()
    