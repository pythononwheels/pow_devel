#!python
#  pow app generator
#  Generates the PoW Application.
#  options are:
#   see: python generate_app.py --help


from optparse import OptionParser
import sqlite3, sys, os, datetime
import string
import shutil

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./stubs/lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./stubs/models/powmodels" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./scripts" )))
for p in sys.path:
    print p
    

import powlib
import generate_model
    
def main():
    """ 
        Executes the render methods to generate a conroller and basic 
        tests according to the given options 
    """
    parser = OptionParser()
    #mode = MODE_CREATE
    parser.add_option("-n", "--name",  action="store", type="string", dest="name", 
        help="set the app name", default ="None")
    parser.add_option("-d", "--directory",  action="store", type="string", dest="directory", 
        help="app base dir", default ="./")
    parser.add_option("-f", "--force",  action="store_true",  dest="force", 
        help="forces overrides of existing app", default="False")

    (options, args) = parser.parse_args()
    #print options, args
    if options.name == "None":
        if len(args) > 0:
            # if no option flag (like -n) is given, it is assumed that 
            # the first argument is the appname. (representing -n arg1)
            options.name = args[0]
        else:
            parser.error("You must at least specify an appname by giving -n <name>.")
    
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
    
    infile = open("./stubs/config/db.py")
    instr = infile.read()
    infile.close()
    instr = instr.replace("please_rename_the_development_db", appname + "_devel")
    instr = instr.replace("please_rename_the_test_db", appname + "_test")
    instr = instr.replace("please_rename_the_production_db", appname + "_prod")
    ofile = open( os.path.normpath(appbase + "/config/db.py"), "w" )
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
                        {"migrations" : [] },
                        {"models" : ["basemodels"] },
                        {"controllers" : [] },
                        {"public" : ["img", "img/bs", "ico", "css", "css/bs", "js", "js/bs", "doc"] },
                        {"stubs" : ["partials"] },
                        {"views" : ["layouts"] },
                        {"tests" : ["models", "controllers", "integration", "fixtures"] },
                        {"ext" : ["auth", "validate"] }                        
                        ]
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
                        ("stubs/migrations","migrations"),
                        ("stubs/partials","stubs/partials"),
                        ("stubs/public/doc","/public/doc"),
                        ("stubs/public/ico","/public/ico"),
                        ("stubs/public/img","/public/img"),
                        ("stubs/public/img/bs","/public/img/bs"),
                        ("stubs/public/css","/public/css"),
                        ("stubs/public/css/bs","/public/css/bs"),
                        ("stubs/public/js", "public/js"),
                        ("stubs/public/js/bs", "public/js/bs"),
                        ("stubs/lib", "lib"), 
                        ("stubs/controllers", "controllers"),
                        ("stubs/views", "views"),
                        ("stubs/views/layouts", "views/layouts"),
                        ("stubs/ext/auth", "ext/auth"),
                        ("stubs/ext/validate", "ext/validate"),
                        ]
                        
    print " -- copying files ..."
    exclude_patterns = [".pyc", ".pyo", ".DS_STORE"]
    exclude_files = [ "db.cfg" ]
    for source_dir, dest_dir in deep_copy_list:
        for source_file in os.listdir(source_dir):
            fname, fext = os.path.splitext(source_file)
            if not fext in exclude_patterns and not source_file in exclude_files:
                powlib.check_copy_file(
                    os.path.join(source_dir,source_file),
                    os.path.join(appbase+"/"+dest_dir,source_file)
                )
            else:
                print " excluded:.EXCL", source_file
                continue
                
    #
    # copy the generator files
    #
    powlib.check_copy_file("scripts/generate_model.py", appbase)
    powlib.check_copy_file("scripts/do_migrate.py", appbase)
    powlib.check_copy_file("scripts/generate_controller.py", appbase)
    powlib.check_copy_file("scripts/generate_migration.py", appbase)
    powlib.check_copy_file("scripts/generate_scaffold.py", appbase)
    powlib.check_copy_file("scripts/generate_mvc.py", appbase)
    powlib.check_copy_file("scripts/simple_server.py", appbase)
    powlib.check_copy_file("pow_router.wsgi", appbase)
    powlib.check_copy_file("scripts/pow_console.py", appbase)
    powlib.check_copy_file("scripts/runtests.py", appbase)
        
    powlib.replace_string_in_file(
        os.path.join(appbase + "/" + "simple_server.py"),
        "#POWAPPNAME",
        appname
    )
    
    powlib.replace_string_in_file(
        os.path.join(appbase + "/" + "pow_router.wsgi"),
        "#POWAPPNAME",
        appname
    )
    
    #
    # copy the initial db's
    #
    appdb = "stubs/db/app_db_including_app_versions_small.db"
    powlib.check_copy_file(appdb, os.path.normpath(appbase + "/db/" + appname + "_prod.db") )
    powlib.check_copy_file(appdb, os.path.normpath(appbase + "/db/" + appname + "_test.db") )
    powlib.check_copy_file(appdb, os.path.normpath(appbase + "/db/" + appname + "_devel.db") )
    #powlib.check_copy_file("stubs/db/empty_app.db", os.path.normpath(appbase + "/db/app.db") )
    
    #
    # initiate the db.cfg file
    #
    render_db_config(appname, appbase)
    
    generate_model.render_model("App", False, "System class containing the App Base Informations", appname)
    generate_model.render_model("Version", False, "System class containing the Versions", appname)
    return
    
    
if __name__ == "__main__":
    main()