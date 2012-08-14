#  pow migration generator.
#
# options are: 
#   see: python generate_migration.py --help


import os, datetime, time
from optparse import OptionParser
import sqlite3
import sys
import datetime
from sqlalchemy.orm import mapper
from sqlalchemy import *

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models" )))

import powlib
import App

# setting the right defaults
MODE_CREATE = 1
MODE_REMOVE = 0
PARTS_DIR = powlib.PARTS_DIR


def main():
    parser = OptionParser()
    mode= MODE_CREATE
    parser.add_option("-n", "--name",  action="store", type="string", dest="name", help="creates migration with name = <name>. Only for jobs", default ="None")
    parser.add_option("-m", "--model",  action="store", type="string", dest="model", help="defines the model for this migration.", default ="None")
    parser.add_option("-c", "--comment",  action="store", type="string", dest="comment", help="defines a comment for this migration.", default ="No Comment")
    parser.add_option("-j", "--job",  action="store", type="string", dest="job", help="creates migration job, e.g for backups, restores etc.",default="None")
    parser.add_option("-d", "--column-definitions",  action="store", 
                        type="string", dest="col_defs", 
                        help="column definitions.Form: d- 'NAME TYPE opt, NAME2 TYPE2 opt2' Name, type, options (all SQLAlchemy style).",
                        default="None")
    #
    # column definition format: NAME TYPE opt1 opt2 optn, NAME2 TYPE2 opt1 opt2 optn ....
    # 
    

    (options, args) = parser.parse_args()
    #print options
    #TODO: reorg and optimie the section below. more structure.
    #
    if options.model == "None" and options.job == "None":
        if len(args) > 0:
            # if no option flag (like -m) is given, it is assumed that the first argument is the model. (representing -m arg1)
            options.model = args[0]
            migration_name = options.model
            migration_model = options.model
        else:
            parser.error("You must at least specify an migration name by giving -n <name>.")
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
        render_migration(migration_name, migration_model,options.comment, options.col_defs)
    
    end = datetime.datetime.now()
    duration = None
    duration = end - start 
    
    print "generated_migration in("+ str(duration) +")"
    return

def transform_col_defs( ostr, col_defs ):
    """
        Get the list of given column definitions of the form:
        
            NAME TYPE opt1 opt2 optn, NAME2 TYPE2 opt1 opt2 optn ....
        And transform them to a valid SQLAlchemy Column definition for a migration.
        Form:
            Column('firstname', String(150), Options)
        
    """
    
    cols = ""
    clist = str(col_defs).split(",")
    print clist
    counter = 0
    for elem in clist:
        counter += 1
        elem = elem.strip()
        elem = elem.split(" ")
        if len(elem) == 2:
            cols += "Column('%s', %s)" % (elem[0], elem[1]) 
        elif len(elem) == 3:
            cols += "Column('%s', %s, %s)" % (elem[0], elem[1], elem[2])
        else:
            print "Error. Wrong number of arguments. You must give name, type (and optionally column options)"
        if counter < len(clist):
            cols += "," + os.linesep + powlib.tab*3

    ostr = ostr.replace("Column('example_column', String(50))", cols)
    
    return ostr
       
def render_migration(name, model, comment, col_defs = "", PARTS_DIR = powlib.PARTS_DIR, prefix_dir = "./"):
    # 
    #print "generate_migration: " + name + "  for model: " + model
    #
    
    # add the auto generated (but can be safely edited) warning to the outputfile
    infile = open (os.path.normpath(PARTS_DIR + "/can_be_edited.txt"), "r")
    ostr = infile.read()
    infile.close()
    
    # add a creation date
    ostr = ostr + os.linesep
    ostr = ostr + "# date created: \t" + str(datetime.date.today())
    ostr = ostr + os.linesep
    
    # Add the model_stub part1 content to the newly generated file. 
    infile = open (os.path.normpath( PARTS_DIR + "db_migration_stub2_part1.py"), "r")
    ostr = ostr + infile.read()
    infile.close()
    
    pluralname = powlib.plural(model)
    ostr += powlib.tab +  "table_name=\"" + pluralname + "\""
    ostr += powlib.linesep
    #print "modelname was: " + model + "  pluralized table_name is:" + pluralname
    
    # Add the model_stub part2 content to the newly generated file. 
    infile = open (os.path.normpath( PARTS_DIR + "db_migration_stub2_part2.py"), "r")
    ostr = ostr + infile.read()
    infile.close()
    
    #
    # Add / Replace the column definitions with the given ones by -d (if there were any)
    # 
    if col_defs != "None":
        ostr = transform_col_defs( ostr, col_defs )
        
    app = powlib.load_class( "App", "App")
    app_versions = powlib.load_class( "Version", "Version")
    sess = app.pbo.getSession()
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
    ofile = open(  os.path.normpath(os.path.join(prefix_dir,filename)) , "w+") 
    print  " -- created file:" + str(os.path.normpath(os.path.join(prefix_dir,filename)))
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
        powlib.check_copy_file(os.path.normpath( PARTS_DIR + "migration_job.py"), "./migrations/" + filename + "_migration.py")
        return
        



if __name__ == '__main__':
    main()
