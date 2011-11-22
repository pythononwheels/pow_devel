#
# generates the bang app skeleton
#

import generate_migration
import generate_model
import generate_scaffold
import generate_controller
import sys,os, os.path
import do_migrate

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))

import powlib

if __name__ == "__main__":
	generate_model.render_model("user", True, "User Model")
	generate_migration.render_db_migration("user", "user", "User Migration")
	do_migrate.do_migrate(-1, "up")
	generate_controller.renderController("user", True)
	generate_scaffold.scaffold("user", True)