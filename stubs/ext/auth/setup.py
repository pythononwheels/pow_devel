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
import powlib
import ext

if __name__ == "__main__":
    
    print "setup plugin: Auth"
    #
    # Copy the Controller
    #
    print " -- copying the Controller... to " + os.path.normpath("../../" + ext.auth["controllers_dir"])
    powlib.check_copy_file("AuthController.py",os.path.join("../../" + ext.auth["controllers_dir"],"AuthController.py") )
    
    #
    # Copy the Views
    #
    print " -- copying the Views... to " + os.path.normpath("../../" + ext.auth["views_dir"])
    for elem in ["User_create.tmpl", "User_edit.tmpl", "User_list.tmpl","User_message.tmpl", "User_show.tmpl"]:
        powlib.check_copy_file( elem ,os.path.join("../../" + ext.auth["views_dir"], elem))
        print " -- -- ", elem
        
    
    #
    # Generate The Model
    #
    print " -- generating the User model."
    generate_model.render_model("user", False, "User model for py_auth", "../../", None, "../../stubs/partials/")
    
    
    
    #
    # render the user migration
    #
    col_defs = "firstname String(100),"
    col_defs += "lastname String(100),"
    col_defs += "email String(100),"
    col_defs += "password String(20),"
    col_defs += "login String(20)"
    generate_migration.render_migration("user", "user", "user model for py_auth", col_defs, "../../stubs/partials/", "../../")
    
    
    