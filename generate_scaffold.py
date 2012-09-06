
#  pow scaffold generator.
#
#  options are: 
#    no option or -create         means create
#    -remove             removes 

import email
import string
import os
from optparse import OptionParser
import sqlite3
import sys
import datetime
from sqlalchemy.orm import mapper
from sqlalchemy import *


sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models/powmodels" )))
import powlib


# setting the right defaults
MODE_CREATE = 1
MODE_REMOVE = 0
PARTS_DIR = powlib.PARTS_DIR

def main():
    """ Executes the render methods to generate scaffold views for a model according to the given options """
    parser = OptionParser()
    mode = MODE_CREATE    
    parser.add_option(  "-m", "--model",  
                        action="store", 
                        type="string", 
                        dest="model", 
                        help="defines the model for this migration.", 
                        default ="None")
    parser.add_option(  "-f", "--force",  
                        action="store_true",  
                        dest="force", 
                        help="forces overrides of existing files",
                        default=False)

    start = None
    end = None
    start = datetime.datetime.now()
    
    (options, args) = parser.parse_args()
    print options
    if options.model == "None":
        if len(args) > 0:
            # if no option flag (like -n) is given, it is 
            # assumed that the first argument is the model name. (representing -n arg1)
            options.model = args[0]
        else:
            parser.error("You must at least specify an appname by giving -n <name>.")
    
    scaffold(options.model, options.force)
    end = datetime.datetime.now()
    duration = None
    duration = end - start 
    print "generated_scaffold in("+ str(duration) +")"
    return
    
def scaffold(   modelname, 
                force, 
                actions = ["list", "show","create", "edit", "message"], 
                PARTS_DIR = powlib.PARTS_DIR, 
                prefix_dir = "./" ):
    """
        Generates the scaffold view for a given model.
        @param modelname:  the name of the model for which the views are scaffolded
        @param force:      if set, existing files will be overwritten (default=False)
        @param actions:    list of actions for which the views will be scaffoded
        @param PARTS_DIR:  relative path of the stubs/partial directory. (default=stubs/partials)
        @param prefix_dir: prefix_path for the generated views. /(default=./ which results in ./views) 
    """
     
    print "generating scaffold for model: " + str(modelname)
    
    for act in actions:
       
        # Add the _stub part0 content to the newly generated file. 
        infile = open (os.path.normpath( PARTS_DIR +  "scaffold_stub_part0.tmpl"), "r")
        ostr = infile.read()
        infile.close() 
        
        # add a creation date
        ostr = ostr.replace("#DATE", str(datetime.date.today()) )        
       
        
        # Add the _stub part1 content to the newly generated file. 
        infile = open (os.path.normpath( PARTS_DIR +  "scaffold_" + act +"_stub_part1.tmpl"), "r")
        ostr = ostr + infile.read()
        infile.close()
        filename = string.capitalize(modelname)  + "_" + act +".tmpl"
        filename = os.path.normpath( 
                            os.path.join(prefix_dir + "/views/", filename) ) 
                                    
        #TODO: optimize the double else part .
        if os.path.isfile( os.path.normpath(filename) ):
            if not force:
                print filename + " already exists..."
            else:
                ofile = open(  filename , "w+") 
                print  " -- created scaffold " + filename
                ofile.write( ostr )
                ofile.close()
        else:
            ofile = open(  filename , "w+") 
            print  " -- created scaffold " + filename
            ofile.write( ostr )
            ofile.close()
            
    return
    

if __name__ == '__main__':
    main()
