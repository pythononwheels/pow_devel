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
    
    
    if not powlib.check_for_file("./", "exec_once.nfo"):
       print "#########################################################################" 
       print "# ==> plugin has not been setup, yet. Nothing to be done."       
       print "#########################################################################"
       sys.exit()
       
    print "###################################################################"
    print "# cleaning up auth plugin has to be done manually"
    print "# this is not done automatically to prevent "
    print "# deleting migrations occured inbetween aut install and this attemp "
    print "# to delete it."
    print "#"
    print "# 1. migrate down to the migration before the user migration"
    print "# 2. remove the user_migration (using do_migrate -e)"
    print "# 3. remove the file: exec_once.nfo in the ext/auth directory"
    print "##################################################################"
    