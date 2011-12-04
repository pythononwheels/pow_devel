#!C:\Python26\python.exe -u

#  pow model generator.
#
# options are: 
#	no option or -create 		means create
#	-remove 			removes 


import os, datetime, time
from optparse import OptionParser
import sqlite3
import sys
import datetime
from sqlalchemy.orm import mapper
from sqlalchemy import *

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models/powmodels" )))
import powlib
import App

# setting the right defaults
MODE_CREATE = 1
MODE_REMOVE = 0

def main():
	parser = OptionParser()
	mode= MODE_CREATE
	parser.add_option("-n", "--name",  action="store", type="string", dest="name", help="creates migration with name = <name>. Only for jobs", default ="None")
	parser.add_option("-m", "--model",  action="store", type="string", dest="model", help="defines the model for this migration.", default ="None")
	parser.add_option("-c", "--comment",  action="store", type="string", dest="comment", help="defines a comment for this migration.", default ="No Comment")
	parser.add_option("-j", "--job",  action="store", type="string", dest="job", help="creates migration job, e.g for backups, restores etc.",default="None")

	(options, args) = parser.parse_args()
	#print options
	if options.model == "None" and options.job == "None":
		parser.error("You must at least specify a migration model by giving -m <modelname>.")
		return
	else:
		if options.name == "None":
			migration_name = options.model
		else:
			migration_name = options.name
			#migration_name = options.name
		migration_model = options.model
	start = None
	end = None
	start = datetime.datetime.now()
	
	if options.job != "None":
		render_migration_job(options.job)
	else:
		render_migration(migration_name, migration_model,options.comment)
	
	end = datetime.datetime.now()
	duration = None
	duration = end - start 
	
	print "generated_migration in("+ str(duration) +")"
	return
	
def render_migration(name,model, comment):
	# 
	
	#print "generate_migration: " + name + "  for model: " + model
	
	# add the auto generated warning to the outputfile
	infile = open (os.path.normpath("./stubs/can_be_edited.txt"), "r")
	ostr = infile.read()
	infile.close()
	
	# add a creation date
	ostr = ostr + os.linesep
	ostr = ostr + "# date created: \t" + str(datetime.date.today())
	ostr = ostr + os.linesep
	
	# Add the model_stub part1 content to the newly generated file. 
	infile = open (os.path.normpath("./stubs/db_migration_stub2_part1.py"), "r")
	ostr = ostr + infile.read()
	infile.close()
	
	pluralname = powlib.plural(model)
	ostr += powlib.tab +  "table_name=\"" + pluralname + "\""
	ostr += powlib.linesep
	#print "modelname was: " + model + "  pluralized table_name is:" + pluralname
	
	# Add the model_stub part2 content to the newly generated file. 
	infile = open (os.path.normpath("./stubs/db_migration_stub2_part2.py"), "r")
	ostr = ostr + infile.read()
	infile.close()
	
	#ostr += powlib.tab + powlib.tab + powlib.tab +  "Column('id', Integer, Sequence('" + model +"_id_seq'), primary_key=True),"
	#ostr += powlib.newline
	
	app = powlib.load_class( "App", "App")
	app_versions = powlib.load_class( "Version", "Version")
	sess = app.pao.getSession()
	app = sess.query(App.App).first()
	
	version = app.maxversion
	oldmaxversion = version
	version += 1
	
	verstring = powlib.version_to_string(version)
	print "generate_migration: " + name + " for model: " + model
	#print "version: " + str(version)
	#print "version2string: " + verstring
	filename = os.path.normpath ( "./migrations/" + verstring +"_" + name +".py" )
	
	#update the app table with the new version
	#appTable.update().values(maxversion= str(version) ).execute()
	app.maxversion = str(version)
	app.update()
	app_versions.filename = str(verstring +"_" + name )
	app_versions.version = str(version)
	app_versions.comment = str(comment)
	app_versions.update()
	print " -- maxversion (old,new): (" + str(oldmaxversion) + "," + str(app.maxversion) +")"
	ofile = open(  filename , "w+") 
	print  " -- created file:" + str(filename)
	ofile.write( ostr )
	ofile.close()
	return
	
def render_migration_job(filename):
		"""create a 'job' or task that has to be done on the database.
		typical examples are backup/restore scripts for dbs or tables or loading data into a table.
		These migrations are not part of the migration versioning system.
		They can be executed with python migrate.py -f <migrationname>
		"""
		print " -- creating migration job:"
		powlib.check_copy_file(os.path.normpath("./stubs/migration_job.py"), "./migrations/" + filename + "_migration.py")
		return
		



if __name__ == '__main__':
	main()
