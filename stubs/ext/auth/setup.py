#
# Standard setup script to enable this plugin in PoW
#
import sys
import os
import os.path

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../modules" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../" )))

import generate_migration
import generate_model
import generate_scaffold
import powlib
import ext

if __name__ == "__main__":
    
    print "setup plugin: Auth"
    #
    # Copy the Controllers
    #
    print " -- copying the AuthController... to " + os.path.normpath("../../" + ext.auth["controllers_dir"])
    powlib.check_copy_file("AuthController.py",os.path.join("../../" + ext.auth["controllers_dir"],"AuthController.py") )
    rint " -- copying the UserController... to " + os.path.normpath("../../" + ext.auth["controllers_dir"])
    powlib.check_copy_file("UserController.py",os.path.join("../../" + ext.auth["controllers_dir"],"UserController.py") )
    
    
    #
    # Generate The Model
    #
    print " -- generating the User model."
    generate_model.render_model("user", False, "User model for py_auth", "../../", None, "../../stubs/partials/")
    
    
    #
    # render the User views
    #
    generate_scaffold.scaffold("user", True, 
                              actions = ["list", "show","create", "edit", "message"], 
                              PARTS_DIR = "../../stubs/partials/", prefix_dir = "../../" )
    
    #
    # render the user migration
    #
    col_defs = "firstname String(100),"
    col_defs += "lastname String(100),"
    col_defs += "email String(100),"
    col_defs += "password String(20),"
    col_defs += "login String(20)"
    generate_migration.render_migration("user", "user", "user model for py_auth", col_defs, "../../stubs/partials/", "../../")
    
    
    