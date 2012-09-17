#!python
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
import string

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models" )))

import powlib
import App

# setting the right defaults
MODE_CREATE = 1
MODE_REMOVE = 0
PARTS_DIR = powlib.PARTS_DIR

    
def main():
    """ Executes the render methods to generate a migration according to the given options """
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
    #TODO: reorg and optimize the section below. more structure.
    #
    if options.model == "None" and options.job == "None":
        # no model- or job flag given
        if len(args) > 0:
            # if no option flag (like -m) is given, it is assumed 
            #that the first argument is the model. (representing -m arg1)
            options.model = args[0]
            migration_name = options.model
            migration_model = options.model
            if migration_name.startswith("rel_") and ( migration_name.count("_") == 2 ):
                # if the name is of the form: rel_name1_name2 it is assumed that you want to
                # generate a relation between name1 and name2. So the mig is especially customized for that.
                print "assuming you create a relation migration"
                start = None
                end = None 
                start = datetime.datetime.now()
                render_relation_migration(migration_name)
                end = datetime.datetime.now()
                duration = None
                duration = end - start 

                print "generated_migration in("+ str(duration) +")"
                return
        else:
            parser.error("You must at least specify an migration name by giving -n <name>.")
            return
    else:
        # we got a model or job.
        if options.name == "None":
            # if no specifoc name for the migration is given, take the modelname
            migration_name = options.model
        else:
            # else take the specific name
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


def render_relation_migration(name, PARTS_DIR = powlib.PARTS_DIR, prefix_dir = "./"):
    """
    renders a migration for a relational link between tables / models
    Typical examples are A.has_many(B) and B.belongs_to(A)
    these are then added to the newly genrated migration file.
    
    @params name    =>  name of the migration. Must be rel_modelA_modelB
    @param PARTS_DIR:   A relative path to the stubs/partials dir from the executing script.
    @param prefix_dir:  A prefix path to be added to migrations making prefix_dir/migrations the target dir
    """
    splittxt = string.split(name, "_")
    model1 = splittxt[1]
    model2 = splittxt[2]
    
    print " -- generate_migration: relation migration for models: " + model1 +  " & " + model2
    print " -- following the naming convention rel_model1_model2"
    print " -- you gave:", name
    
    # add the auto generated (but can be safely edited) warning to the outputfile
    infile = open (os.path.normpath(PARTS_DIR + "/db_relation_migration_stub.part"), "r")
    ostr = infile.read()
    infile.close()
    
    # add a creation date
    ostr = ostr.replace( "#DATE", str(datetime.date.today() ))
    # add model1 import
    ostr = ostr.replace( "#IMPORT_MODEL1", "import " + model1)
    # add model2 import
    ostr = ostr.replace( "#IMPORT_MODEL2", "import " + model2)
    
    # add the example migration for this models
    ostr = ostr.replace( "#MODEL1", model1)
    ostr = ostr.replace( "#MODEL2_has_many", powlib.pluralize(model2))
    ostr = ostr.replace( "#MODEL2", model2)
    
    filename = write_migration( name, 
                                "relation between %s and %s" % (model1, model2),
                                prefix_dir,
                                ostr
                                )
    print  " -- created file:" + str(os.path.normpath(os.path.join(prefix_dir,filename)))
    return
    

def write_migration(name, comment, prefix_dir, ostr):
    """
    Writes a new migration.
    It generates a new version, constructs the correct filename and path
    Updates the App and Version tables and writes ostr to the new filen.
    @param name:    Name of the new migration. 
    @param ostr:    Content that will be written to the new migration.
    """
    version = get_new_version()
    verstring = powlib.version_to_string(version)
    # will be saved in the versions table and used to load the module by do_migrate
    modulename = verstring +"_" + name 
    filename = modulename + ".py"
    
    #update the app table with the new version
    update_app_and_version(version, modulename, version, comment )
    
    ofile = open(  os.path.normpath(os.path.join(prefix_dir + "/migrations/", filename)) , "w+") 
    ofile.write(ostr)
    ofile.close()
    return filename
    
def get_new_version():
    """
    Constructs the new version by queriing the App Table for maxversion
    """
    app = powlib.load_class( "App", "App")
    
    sess = app.pbo.getSession()
    app = sess.query(App.App).first()
    
    version = app.maxversion
    version += 1
    return version
    
def update_app_and_version(maxversion, filename, version, comment=""):
    """
    update the app table with the new version
    update the version table with:
        filename, version and comment (if any).
    """
    app = powlib.load_class( "App", "App")
    app_versions = powlib.load_class( "Version", "Version")
    app = app.find_first()
    app.maxversion = str(maxversion)
    app.update()
    app_versions.filename = str(filename)
    app_versions.version = str(version)
    app_versions.comment = str(comment)
    app_versions.update()
    return 
    
def render_migration(name, model, comment, col_defs = "", PARTS_DIR = powlib.PARTS_DIR, prefix_dir = "./"):
    """
    Renders a database migration file.
    @param name:        A Name for the migration. By default the modelname is taken.
    @param model:       Modelname for this migration (typically defining the model's base table)
    @param comment:     a Comment for this migration
    @param col_defs:    pre defined column definitions of the form NAME TYPE OPTIONS, NAME1 TYPE1 OPTIONS1, ...
    @param PARTS_DIR:   A relative path to the stubs/partials dir from the executing script.
    @param prefix_dir:  A prefix path to be added to migrations making prefix_dir/migrations the target dir
    """
    
    # add the auto generated (but can be safely edited) warning to the outputfile
    infile = open (os.path.normpath(PARTS_DIR + "/db_migration_stub.part"), "r")
    ostr = infile.read()
    infile.close()

    # Replace the TAGGED Placeholders with the actual values
    ostr = ostr.replace( "#DATE", str(datetime.date.today() ))
    pluralname = powlib.plural(model)
    ostr = ostr.replace("#TABLENAME", pluralname)
    
    #
    # Add / Replace the column definitions with the given ones by -d (if there were any)
    # 
    if col_defs != "None":
        ostr = transform_col_defs( ostr, col_defs )

    # generate the new version
    version = get_new_version()
    verstring = powlib.version_to_string(version)

    print "generate_migration: " + name + " for model: " + model

    # really write the migration now
    write_migration(name, comment, prefix_dir, ostr)

    return


def render_migration_job(filename):
        """create a 'job' or task that has to be done on the database.
        typical examples are backup/restore scripts for dbs or tables or loading data into a table.
        These migrations are not part of the migration versioning system.
        They can be executed with python migrate.py -f <migrationname>
        """
        print " -- creating migration job:"
        powlib.check_copy_file(os.path.normpath( PARTS_DIR + "migration_job.part"), "./migrations/" + filename + "_migration.py")
        return
        

if __name__ == '__main__':
    main()
