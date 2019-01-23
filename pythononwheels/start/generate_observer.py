#
# generate model observer
#

import argparse
import tornado.template as template
import os
from {{appname}}.config import templates
from {{appname}}.powlib import pluralize
from pydoc import locate

def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def generate_observer(model_name=None, model_type=None, appname=None):
    """ generates a basic observer
    """
    #
    # set some attributes
    #
    print(40*"-")
    print(" generating observer: " + model_name)
    print(40*"-")
    try:
        loader = template.Loader(templates["stubs_path"])
        model_class_name = camel_case(model_name)
        print("model_class_name: " + model_class_name)
        #
        # create the model
        #
        ofilePath = os.path.join(templates["model_path"], model_type)
        ofile = open(os.path.join(ofilePath, model_name + "_observer.py"), "wb")
        try:
            res = loader.load("model_observer.py").generate( 
                model_name=model_name, 
                model_class_name=model_class_name,
                appname=appname,
                model_type=model_type
                )
            ofile.write(res)
            ofile.close()
        except Exception as e:
            print(str(e))
    except:
        return False
    print("... generated: " + model_type + " observer")
    print(40*"-")
    print("... in : " + ofile.name)
    print(40*"-")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", action="store", 
                        dest="name", help='-n modelname',
                        required=True)
    parser.add_argument('-t', "--type", action="store", 
                        dest="type", help='-d dbtype   -> Example: -d sql  OR -d tinydb ...',
                        default="sql", required=True)
    #
    # db type
    # 
    # parser.add_argument('-d', "--db", action="store", 
    #                     dest="db", help='-d which_db (mongo || tiny || peewee_sqlite) default = tiny',
    #                     default="tiny", required=True)
    args = parser.parse_args()
    #
    # show some args
    #
    #print("all args: ", args)
    #print(dir(args))
    #print("pluralized model name: ", pluralize(args.name))
    generate_observer(model_name=args.name, model_type=args.type, appname="{{appname}}")

if __name__ == "__main__":
    main()