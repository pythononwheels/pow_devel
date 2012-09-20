
#!python
#  pow migration generator.
#
# options are: 
#   see: python generate_migration.py --help


import os 
import datetime 
import time
from optparse import OptionParser
import sys
import string

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(__file__), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(__file__), "./models" )))

import powlib
import generate_migration
import generate_model
import generate_scaffold
import generate_controller
import powlib

# setting the right defaults
MODE_CREATE = 1
MODE_REMOVE = 0
PARTS_DIR = powlib.PARTS_DIR


def main():
    """ Executes the render methods to generate a model, controller, 
    migration and the views according to the given options """
    parser = OptionParser()
    mode= MODE_CREATE
    parser.add_option("-m", "--model",  
                      action="store", 
                      type="string", 
                      dest="model", 
                      help="defines the model for this migration.", 
                      default ="None")
    
    parser.add_option("-c", "--comment",  
                      action="store", 
                      type="string", 
                      dest="comment", 
                      help="defines a comment for this migration.", 
                      default ="No Comment")
    
    parser.add_option("-d", "--column-definitions",  
                      action="store", 
                      type="string", dest="col_defs", 
                      help="""column definitions.Form: d- 'NAME TYPE opt, NAME2 TYPE2 opt2' 
                              Name, type, options (all SQLAlchemy style).""",
                      default="None")
     
    parser.add_option("-f", "--force",  
                        action="store_true",  
                        dest="force", 
                        help="forces overrides of existing files",
                        default=False)
    #
    # column definition format: NAME TYPE opt1 opt2 optn, NAME2 TYPE2 opt1 opt2 optn ....
    # 
    start = datetime.datetime.now()
    
    
    (options, args) = parser.parse_args()
    
    #if no model given and no parameter at all, then quit with error
    if options.model == "None" and len(args) < 1:
        parser.error("You must at least specify an migration name by giving -n <name>.")
        return
    else:
        # if no model given but a parameter, than assume that the first parameter 
        # is the model
        if options.model == "None":
            options.model = args[0]
        
        print "generate_mvc for model:", options.model
        # generate the model
        generate_model.render_model(modelname = options.model, 
                                    force = options.force, 
                                    comment = options.comment
                                    )
        print
        # generate the Controller
        generate_controller.render_controller( name = options.model,
                                               force = options.force
                                              )
        
        print
        # generate the views
        generate_scaffold.scaffold(modelname = options.model, 
                                   force = options.force, 
                                   actions = ["list", "show","create", "edit", "message"]
                                   ) 
                                   
        print
        # generate the migration
        # ooptions_col_defs has to be a comma separated list of column names and SQLAlchemy DB types:
        # example: lastname String(100), email String(100)
        col_defs = options.col_defs
        
        generate_migration.render_migration( modelname = options.model, 
                                             comment = options.comment, 
                                             col_defs = options.col_defs
                                             ) 
        print                                
        
    
    end = datetime.datetime.now()
    duration = end - start 
    print "generated_mvc in("+ str(duration) +")"
    print 
    return

if __name__ == "__main__":
    main()
    sys.exit(0)