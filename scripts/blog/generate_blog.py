#
# automates the (few) manual steps needed to
# setup a base weblog environment for PoW.
#
# khz (July/2012)
#


import generate_migration
import generate_model
import generate_scaffold
import generate_controller
import sys,os, os.path
import do_migrate

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))

import powlib

def generate_all_for( model ):
    generate_model.render_model(model, True, model + " Model")
    generate_controller.render_controller(model, True)
    generate_scaffold.scaffold(model, True)    
    generate_migration.render_migration(model, model, model + " Migration")
    return


if __name__ == "__main__":
    generate_all_for( "post" )
    #do_migrate.do_migrate(-1, "up")
    
    #do_migrate.do_migrate(-1, "up")
    print " -----------------------------------------------------------"
    print " .. everything has been created, you need to migrate up 2 times"
    print " .. this is not done automatically, since you might want to change the" 
    print " .. tables first."
    print " => see: ./migrations/ folder"
    sys.exit(0)