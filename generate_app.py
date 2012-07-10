#!C:\Python26\python.exe -u

#  pow model generator.
#
# options are:
#    no option or -create         means create
#    -remove             removes

from optparse import OptionParser
import sqlite3, sys, os, datetime
import string
import shutil

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./stubs/lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./stubs/models/powmodels" )))
import powlib


# setting the right defaults
#MODE_CREATE = 1
#MODE_REMOVE = 0

#pow_newline = powlib.linesep
#pow_tab = powlib.tab

    
def main():
    parser = OptionParser()
    #mode = MODE_CREATE
    parser.add_option("-n", "--name",  action="store", type="string", dest="name", 
        help="set the app name", default ="None")
    parser.add_option("-d", "--directory",  action="store", type="string", dest="directory", 
        help="app base dir", default ="./")
    parser.add_option("-f", "--force",  action="store_true",  dest="force", 
        help="forces overrides of existing app", default="False")
    #parser.add_option("-c", "--comment",  action="store", type="string", dest="comment", 
        #help="defines a comment for this migration.", default ="No Comment")


    (options, args) = parser.parse_args()
    #print options, args
    if options.name == "None":
        if len(args) > 0:
            # if no option flag (like -n) is given, it is assumed that the first argument is the appname. (representing -n arg1)
            options.name = args[0]
        else:
            parser.error("You must at least specify an appname by giving -n <name>.")
    
    modelname = options.name
    appdir = options.directory
    appname = options.name
    force = options.force
    start = None
    end = None
    start = datetime.datetime.now()

    gen_app(appname, appdir, force)

    end = datetime.datetime.now()
    duration = None
    duration = end - start
    print " -- generated_app in("+ str(duration) +")"

def render_db_config( appname, appbase ):
    """ Creates the db.cfg file for this application and puts it in appname/config/db.cfg"""
    infile = open("./stubs/config/db.cfg")
    instr = infile.read()
    infile.close()
    instr = instr.replace("please_rename_the_development_db", appname + "_devel")
    instr = instr.replace("please_rename_the_test_db", appname + "_test")
    instr = instr.replace("please_rename_the_production_db", appname )
    ofile = open( os.path.normpath(appbase + "/config/db.cfg"), "w" )
    ofile.write(instr)
    ofile.close()
    

def gen_app(appname, appdir, force=False):
    """ Generates the complete App Filesystem Structure for Non-GAE Apps.
        Filesystem action like file and dir creation, copy fiels etc. NO DB action in this function 
    """
    
    appname = str(appname)
    appname = str.strip(appname)
    appname = str.lower(appname)
    print " -- generating app:", appname

    powlib.check_create_dir(appdir + appname)
    appbase = os.path.abspath(os.path.normpath(appdir +"/"+ appname + "/"))
    #print appbase
    # defines the subdirts to be created. Form { dir : subdirs }
    subdirs = [ {"config" : [] },  
                        {"db" : [] },
                        {"lib" : [] },
                        {"migrations" : ["backup"] },
                        {"models" : ["basemodels", "basemodels/pow", "powmodels"] },
                        {"controllers" : [] },
                        {"public" : ["media", "media/images", "media/images/pow_home", "media/images/simple_blog", "media/documents", "scripts", "stylesheets"] },
                        {"stubs" : [] },
                        {"views" : ["layouts"] },
                        {"tests" : ["models", "controllers", "integration", "fixtures"] } ]
    for elem in subdirs:
        for key in elem:
            subdir = os.path.join(appbase,str(key))
            powlib.check_create_dir( subdir)
            for subs in elem[key]:
                powlib.check_create_dir( os.path.join(subdir,str(subs)))
    
    #
    # copy the files in subdirs. Form ( from, to )
    #
    deep_copy_list = [  ("stubs/config", "config"),  
                        ("stubs/lib", "lib"), 
                        ("stubs", "stubs"),
                        ("stubs/public/stylesheets", "public/stylesheets"),
                        ("stubs/public/media","/public/media"),
                        ("stubs/public/media/images","/public/media/images"),
                        ("stubs/public/media/images/pow_home","/public/media/images/pow_home"),
                        ("stubs/public/media/images/simple_blog","/public/media/images/simple_blog"),
                        ("stubs/public/scripts", "public/scripts"),
                        ("stubs/lib", "lib"), 
                        ("stubs/controllers", "controllers"),
                        ("stubs/views", "views"),
                        ("stubs/views/layouts", "views/layouts")
                        ]
    print " -- copying files ..."
    exclude_patterns = [".pyc", ".pyo", ".DS_STORE"]
    exclude_files = [ "db.cfg" ]
    for source_dir, dest_dir in deep_copy_list:
        for source_file in os.listdir(source_dir):
            #print "ext:", os.path.splitext(source_file)
            #print "source:", os.path.abspath(source_file), " is file:", os.path.isfile(os.path.abspath(source_file))
            fname, fext = os.path.splitext(source_file)
            if not fext in exclude_patterns and not source_file in exclude_files:
                #print " copying src:", os.path.join(source_dir,source_file)
                #print "   -> to dest:", os.path.join(appbase,source_file)
                #print "ext:", os.path.splitext(source_file)
                powlib.check_copy_file(
                    os.path.join(source_dir,source_file),
                    os.path.join(appbase+"/"+dest_dir,source_file)
                )
            else:
                print " excluded:.EXCL", source_file
                continue
                
    #print "...done"

    #
    # copy the generator files
    #
    #powlib.check_copy_file("generate_app.py", appbase)
    powlib.check_copy_file("generate_model.py", appbase)
    powlib.check_copy_file("do_migrate.py", appbase)
    powlib.check_copy_file("generate_controller.py", appbase)
    powlib.check_copy_file("generate_migration.py", appbase)
    powlib.check_copy_file("generate_scaffold.py", appbase)
    powlib.check_copy_file("simple_server.py", appbase)
    powlib.check_copy_file("pow_router.wsgi", appbase)
    powlib.check_copy_file("generate_bang.py", appbase)
    powlib.check_copy_file("pow_console.py", appbase)
    powlib.check_copy_file("runtests.py", appbase)

    #
    # copy the initial db's
    #
    powlib.check_copy_file("stubs/db/empty.db", os.path.normpath(appbase + "/db/" + appname + ".db") )
    #powlib.check_copy_file("stubs/db/empty_app.db", os.path.normpath(appbase + "/db/app.db") )
    
    #
    # initiate the db.cfg file
    #
    render_db_config(appname, appbase)
    
    return
    
    
if __name__ == "__main__":
    main()