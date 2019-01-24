#
# generate model observer
#

import argparse
import tornado.template as template
import os
from {{appname}}.config import templates
from {{appname}}.powlib import pluralize
from pydoc import locate
import shutil

def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def generate_dash():
    """ 
        generates a basic dash environment in PythonOnWheels
        handler:        handler/dash.py
        base view:      view/dash_index.tmpl
        dash layout:    pow_dash.py
        componentes:    dash_components.py
    """
    #
    # set some attributes
    #
    print(40*"-")
    print(" generating dash environment: ")
    print(40*"-")
    appname="{{appname}}"
    try:
        loader = template.Loader(templates["stubs_path"])
        #
        # render the dash index view 
        #
        
        try:
            shutil.copy( os.path.join(templates["stubs_path"],"dash_index.tmpl"), 
                os.path.join(templates["views_path"],"dash_index.tmpl"))
            print(" {:15}: {:30}".format("Copied", "the view: dash_index.tmpl"))
        except Exception as e: 
            print(str(e))

        #
        # render the dash handler 
        # 
        ofile = open( os.path.join(templates["handler_path"],"dash_handler.py") , "wb")
        try:
            res = loader.load("dash_handler_template.py").generate( appname=appname )
            ofile.write(res)
            ofile.close()
            print(" {:15}: {:30}".format("rendered", "handler/dash.py"))
        except Exception as e:
            print(str(e))
        
        #
        # render the Dash app and layout file; pow_dash.py
        # 
        ofile = open( os.path.join(".", "pow_dash.py") , "wb")
        try:
            res = loader.load("pow_dash.py").generate( appname=appname )
            ofile.write(res)
            ofile.close()
            print(" {:15}: {:30}".format("rendered", "pow_dash.py [This is the actual Dash layout and Dash app file]"))
        except Exception as e:
            print(str(e))

        #
        # copy the dash_components.py
        #
        try:
            shutil.copy( os.path.join(templates["stubs_path"],"dash_components.py"), os.path.join(".", "dash_components.py" ))
            print(" {:15}: {:30}".format("Copied", "the components file: dash_components.py"))
        except Exception as e:
            print(str(e))
        #
        # copy the dash_requirements.txt
        #
        try:
            shutil.copy( os.path.join(templates["stubs_path"],"dash_requirements.txt"), os.path.join(".", "dash_requirements.txt" ))
            print(" {:15}: {:30}".format("Requirements", "dash_requirements.txt"))
        except Exception as e:
            print(str(e))
    except:
        return False
    
    return True


def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-n', "--name", action="store", 
    #                    dest="name", help='-n modelname',
    #                    required=True)
    
    
    #args = parser.parse_args()
    
    generate_dash()

if __name__ == "__main__":
    main()
    print(40*"-")
    print(" Next Steps:")
    print(40*"-")
    print(" {:15}: {:30}".format("commandline", "pip install -r dash_requirements.txt"))
    print(" {:15}: {:30}".format("commandline", "python server.py"))
    print(" {:15}: {:30}".format("go to", "http://localhost:8080/dash"))
    print()