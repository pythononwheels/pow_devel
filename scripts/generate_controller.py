#!python
#  pow controller generator.
#
# options are: 
#   see: python generate_controller.py --help

import os
from optparse import OptionParser
import sqlite3
import sys
import string
import datetime
from sqlalchemy.orm import mapper
from sqlalchemy import *

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models/powmodels" )))
import powlib
import PowObject

# setting the right defaults
MODE_CREATE = 1
MODE_REMOVE = 0
PARTS_DIR = powlib.PARTS_DIR
CONTROLLER_TEST_DIR = "/tests/controllers/"


def main():
    """ 
        Executes the render methods to generate a conroller and basic 
        tests according to the given options
    """
    parser = OptionParser()
    mode= MODE_CREATE
    parser.add_option("-n", "--name",  action="store", type="string", 
                        dest="name", 
                        help="creates migration with name = <name>", 
                        default ="None")
    parser.add_option("-m", "--model",  
                        action="store", 
                        type="string", 
                        dest="model", 
                        help="defines the model for this migration.", 
                        default ="None")
    parser.add_option("-f", "--force",  
                        action="store_true",  
                        dest="force", 
                        help="forces overrides of existing files",
                        default=False)
    
    controller_name = "None"
    controller_model = "None"
    start = None
    end = None
    start = datetime.datetime.now()
    
    (options, args) = parser.parse_args()
    #print options        
    if options.model == "None":
        if len(args) > 0:
            # if no option flag (like -m) is given, it is assumed that 
            # the first argument is the model. (representing -m arg1)
            options.model = args[0]
        else:
            parser.error("You must at least specify an appname by giving -n <name>.")
            
    controller_name = options.model
    render_controller(controller_name, options.force)

    end = datetime.datetime.now()
    duration = None
    duration = end - start 
    print "generated_controller in("+ str(duration) +")"
    return
    
def render_controller(name, force, prefix_path="./"):
    """ generates a controller according to the given options
        @param name: name prefix of the Controller fullname NameController
        @param force: if true: forces overwrtiting existing controllers"""
    
    print " creating controller: ", name 
    # add the auto generated warning to the outputfile
    infile = open (os.path.normpath(PARTS_DIR + "controller_stub.part"), "r")
    ostr = infile.read()
    infile.close()
    
    #pluralname = powlib.plural(model)
    ostr = ostr.replace( "#DATE", str(datetime.date.today()) )  
    modelname = string.capitalize( name ) 
    ostr = ostr.replace("#MODELNAME", modelname)
    ostr = ostr.replace("#CONTROLLERNAME", modelname)
    classname = modelname + "Controller"
    filename = os.path.normpath ( 
        os.path.join( prefix_path + "./controllers/",  classname + ".py" ) )
    
    if os.path.isfile( os.path.normpath(filename) ):
        if not force:
            print " --", filename,
            print " already exists... (Not overwritten. Use -f to force ovewride)"
        else:
            ofile = open(  filename , "w+") 
            print  " -- created controller " + filename
            ofile.write( ostr )
            ofile.close()
    else:
        ofile = open(  filename , "w+") 
        print  " -- created controller " + filename
        ofile.write( ostr )
        ofile.close()
    #
    # check if BaseController exist and repair if necessary
    if not os.path.isfile(os.path.normpath( "./controllers/BaseController.py")):
        # copy the BaseClass
        powlib.check_copy_file(
            os.path.normpath( "./stubs/controllers/BaseController.py"), 
            os.path.normpath( "./controllers/") )
    
    render_test_stub( name, classname )
    return
    
    
def render_test_stub (controllername, classname, prefix_path ="./" ):
    """ renders the basic testcase for a PoW Controller """
    #print "rendering Testcase for:", classname, " ", " ", modelname
    print " -- generating TestCase...",
    infile = open( os.path.normpath( PARTS_DIR +  "test_controller_stub.part"), "r")
    instr = infile.read()
    infile.close()
    test_name = "Test" + classname + ".py"
    
    ofile = open( 
        os.path.normpath(
            os.path.join(prefix_path + CONTROLLER_TEST_DIR, test_name ) ), "w")
    
    instr = instr.replace("#CLASSNAME", "Test" + classname  )
    instr = instr.replace( "#DATE", str(datetime.date.today()) )  
    ofile.write(instr)
    
    ofile.close()
    print  " %s...(created)" % (prefix_path + CONTROLLER_TEST_DIR + test_name)
    return


if __name__ == '__main__':
    main()
