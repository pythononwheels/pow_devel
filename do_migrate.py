#!C:\Python26\python.exe -u

#  pow model generator.
#
# options are: 
#    no option or -create         means create
#    -remove             removes 


import os
from optparse import OptionParser
import sqlite3, sqlalchemy
import sys
import datetime

from sqlalchemy.orm import mapper

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./controllers" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./migrations" )))

import powlib
import Appinfo
import PowTable

# setting the right defaults
MODE_CREATE = 1
MODE_REMOVE = 0

def main():
    parser = OptionParser()
    mode= MODE_CREATE
    
    parser.add_option("-d", "--direction",  action="store", type="string", dest="direction", help="migrate up or down", default ="None")
    parser.add_option("-v", "--version",  action="store", type="string", dest="version", help="migrates to version ver", default ="None")
    parser.add_option("-e", "--erase",  action="store_true",  dest="erase", help="erases version ver",default="False")
    parser.add_option("-i", "--info",  action="store_true",  dest="info", help="shows migration information",default="False")
    parser.add_option("-j", "--job",  action="store", type="string", dest="job", help="executes a migration job", default ="None")
    parser.add_option("-m", "--method",  action="store", type="string", dest="method", help="execute the given method. Only in combination with -j", default ="None")
    parser.add_option("-s", "--set-currentversion",  action="store", type="string", dest="set_curr_version", help="sets cuurentversion to given version ver", default ="None")
    
    (options, args) = parser.parse_args()
    #print options
    if options.info == True:
        show_info()
        return
    
    if options.version == "None":
        ver = -1
    else:
        ver = int(options.version)
    
    start = None
    end = None
    start = datetime.datetime.now()
    
    if options.erase == True:
        do_erase()
    elif options.set_curr_version != "None":
        set_currentversion( options.set_curr_version )
    elif options.job != "None":
        if options.direction  == "None" and options.method == "None":
            print "You must at least give a direction -d up OR -d down OR a method with -m"
            return
        else:
            do_job(options, options.job, options.method)
    else:
        if options.direction == "None"  and ver == -1:
            print "You must at least give a direction -d up OR -d down"
            return
        else:
            do_migrate(ver, options.direction )
        
    
    end = datetime.datetime.now()
    duration = None
    duration = end - start 
    
    print "migrated in("+ str(duration) +")"


def do_job(options, filename, method):
    print "migrating"
    #print options
    # get rid of trailing directories
    h,t = os.path.split(filename)
    # get rid of file extensions
    filename, ext = os.path.splitext(t)
    #print filename
    # load the class
    mig = powlib.load_class( filename, "Migration" )
    # execute the up() method
    if method != "None":
        eval("mig." + str(method) + "()")
    elif options.direction == "up":
        mig.up()
    elif options.direction == "down":
        mig.down()
    else:
        raise StandardError("Migration Direction is neither <up> nor <down>.")
    return

def do_migrate( goalversion, direction):
    #powlib.load_module("Appinfo")
    print "migrating "
    app = powlib.load_class( "Appinfo", "Appinfo")
    app_versions = powlib.load_class( "Version", "Version")
    sess = app.pbo.getSession()
    app = sess.query(Appinfo.Appinfo).first()
    #print app
    #print "name: " + app.name
    #print "path: " + app.path
    print " -- currentversion: " + str(app.currentversion)
    #print "maxversion: " + str(app.maxversion)
    
    currentversion = int(app.currentversion)
    maxversion = int(app.maxversion)
    
    times = 1
    if goalversion == -1:
        pass
    elif goalversion > maxversion:
        print " -- Error: version would become greater than Maxversion.. bailing out"
        return
    else:
        print " -- migrating to version:" + str(goalversion)
        # setting number of times to run
        if goalversion <  currentversion:
            direction = "down"
            times = currentversion - goalversion
        elif goalversion >= currentversion:
            direction = "up"
            times = goalversion - currentversion
        else:
            times = 0
        print " -- Running " + str(times) + " times: " 
    sess.add(app)
    
        
    for run in range(0,times):
        #
        # migrate up
        if direction == "up":
            if currentversion > maxversion:
                print " -- Error: version would become greater than Maxversion.. bailing out"
                return
            currentversion += 1
            ver = app_versions.find_by("version", currentversion)
            #filename = os.path.normpath ( powlib.version_to_string(currentversion) +"_" + "migration"  )
            filename = ver.filename
            mig = powlib.load_class( filename, "Migration" )
            mig.up()
            print '{0:18} ==> {1:5} ==> {2:30}'.format(" -- Migration run", str(run+1).zfill(5), filename)
        #
        # migrate down
        #
        elif direction == "down":
            if currentversion <= 0:
                print " -- Error: version would become less than < 0 .. bailing out"
                return

            #filename = os.path.normpath ( powlib.version_to_string(currentversion) +"_" + "migration"  )
            ver = app_versions.find_by("version", currentversion)
            filename = ver.filename
            mig = powlib.load_class( filename, "Migration" )
            mig.down()
            currentversion -= 1
            print '{0:18} ==> {1:5} ==> {2:20}'.format(" -- Migration run",  str(run+1).zfill(5), filename)
        else:
            raise StandardError("Direction must be either up or down")
            
    print " -- setting currentversion to: " + str(currentversion)
    app.currentversion =  currentversion
    #sess.dirty
    sess.commit()
    return

def drop_table(tablename, **kwargs):
    model = PowTable.PowTable()
    modelname = powlib.table_to_model(tablename)
    model = powlib.load_class( modelname, modelname )
    #print type(model)
    #powlib.print_sorted(dir(model))
    if not "checkfirst" in kwargs:
        kwargs["checkfirst"]="False"
        print " -- set checkfirst=", kwargs["checkfirst"]
    model.__table__.drop( **kwargs )
    print " -- dropped table: ", tablename
    return
    
def set_currentversion( ver ):
    
    print "migrating "
    app = powlib.load_class( "Appinfo", "Appinfo")
    app_versions = powlib.load_class( "Version", "Version")
    sess = app.pbo.getSession()
    app = sess.query(Appinfo.Appinfo).first()
    #print app
    #print "name: " + app.name
    #print "path: " + app.path
    print " -- currentversion: " + str(app.currentversion)
    print " -- setting currentversion to: " + str(ver)
    #print "maxversion: " + str(app.maxversion)
    goalversion = int(ver)
    if goalversion >=0 and goalversion <=app.maxversion:
        app.currentversion = ver
    else:
        print " -- ERROR: new currentversion <=0 or >= maxversion"
        return
    sess.commit()
    return
    
    
def do_erase():
    app = powlib.load_class( "Appinfo", "Appinfo")
    app_version = powlib.load_class( "Version", "Version")
    sess = app.pbo.getSession()
    app = sess.query(Appinfo.Appinfo).first()
    print " -- erasing migration version:", str(app.maxversion)

    sess.add(app)
    
    maxversion = int(app.maxversion)
    currversion = int(app.currentversion)
    #
    # only delete a migration file if it is not in use (so the current mig is not baed on it)
    #
    if maxversion == currversion:
        print "cannot delete the currently active migration version. Migrate down first"
        return
    # get the version-info from app.db.version
    ver = app_version.find_by("version", maxversion)
    #sess.add(ver)
    
    filename = ver.filename + ".py"
    filename_pyc = filename + "c"
    
    print "attempting to delete version: " + str(maxversion) + "->" + filename
    if os.path.isfile( os.path.normpath("./migrations/" + filename) ):
        os.remove( os.path.normpath("./migrations/" + filename) )
        print " -- deleted: ", filename
    if os.path.isfile( os.path.normpath("./migrations/" + filename_pyc) ):
        os.remove( os.path.normpath("./migrations/" + filename_pyc) )
        print " -- deleted: ", filename_pyc

    #  delete the app.db.version entry
    ver.delete(ver.id)
    
    maxversion -= 1
    print "setting new currentversion to: " + str(currversion)
    app.maxversion =  maxversion
    print "setting new maxversion to: " + str(maxversion)
    #sess.dirty
    sess.commit()

    

def show_info():
    app = powlib.load_class( "Appinfo", "Appinfo")
    app_versions = powlib.load_class( "Version", "Version")
    sess = app.pbo.getSession()
    app = sess.query(Appinfo.Appinfo).first()
    print "showing migration information for"
    print " -- Appname: " + app.name
    print " -- currentversion is : " + str(app.currentversion)
    print " -- max version is : " + str(app.maxversion)

def getTimes(migv, goalv):
    if migv < goalv:
        pass


if __name__ == '__main__':
    main()
