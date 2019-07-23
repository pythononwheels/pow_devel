#
# generate app
#

import argparse
import tornado.template
import os
import sys
import datetime
import shutil
from pathlib import Path
import uuid
#from .update_conf import update_conf

def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def copy_or_pump(src, dest, copy=False, appname=None, sqlite_path=None, 
            extensions=None, data=None, tinydb_path=None, db_base_path=None,
            dbtype=None, cookie_secret=str(uuid.uuid4()), force=False):
    """
        just copy files or pump them through the template engine before copying to out dir
    """
    if not force and os.path.exists(dest):
        print("    skipping copy_or_pump: exists AND force = False ")
    else:
        if not copy:
            print("    pumping to ----->", dest)
            f = open(src, "r", encoding="utf-8")
            instr = f.read()
            f.close()
            template = tornado.template.Template(instr)
            out = template.generate(  
                    dbtype=dbtype,
                    appname=appname,
                    sqlite_path=sqlite_path,
                    tinydb_path = tinydb_path,
                    db_base_path=db_base_path,
                    current_date=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                    cookie_secret=cookie_secret,
                    extensions=extensions,
                    data=data
                    )
            f = open(dest, "w", encoding="utf-8")
            f.write(out.decode("unicode_escape"))
            f.close()
        else:
            # just copy file
            print("    copying to ----->", dest )
            print("    .. :" + str(shutil.copy( src, dest )))


def generate_app(appname, force=False, outpath="..", dbtype="sql", update_only=False, view_type=None):
    """ generates a small model with the given modelname
        also sets the right db and table settings and further boilerplate configuration.
        Template engine = tornado.templates
    """    
    print("  generating app:" + str(appname))
    import os,sys
    base=os.path.normpath(outpath)

    print("  base: " + base)
    root=os.path.join(os.path.dirname(os.path.abspath(__file__)), "start")
    print("  root: " +  root)
    
    outdir=os.path.normpath(os.path.join(base, appname))
    #outdir = os.path.join(outdir, appname)
    print("  ..creating in: " +  outdir)
    
    os.makedirs(outdir, exist_ok=True)
    template_exts = [".py", ".tmpl"]
    # excluded from template processing.
    exclude_dirs = ["static", "stubs", "views"]
    skip_dirs= ["stuff", "werkzeug"]
    exclude_files=[]
    if update_only:
        # only update pow versions. Leave all non pow or possibly changed stuff untouched
        # maybe add encoders.py, decoders.py to the list in the future.
        exclude_files.extend([ "alembic.ini", "db.sqlite", "tiny.db",
                                "env.py", "shorties.py", "config.py", "powhandler.py", 
                                "powmodel.py", "tinymodel.py", "mongomodel.py" ])
        skip_dirs.extend([ "migrations",  "views", "static" ])

    #
    # walk the root (/pow/start)
    # and copy (for .py and .tmpl pump thru template engine first)
    # all files to the new app dir (appname)
    # 
    db_base_path=os.path.normpath(os.path.abspath(outdir))
    tinydb_path=os.path.normpath(os.path.abspath(os.path.join(outdir, "tiny.db")))
    sqlite_path=os.path.normpath(os.path.abspath(os.path.join(outdir, "db.sqlite")))
    if sys.platform =="win32":
        sqlite_path=sqlite_path.replace("\\", "\\\\")
        tinydb_path=tinydb_path.replace("\\", "\\\\")
        db_base_path=db_base_path.replace("\\", "\\\\")
    elif sys.platform in ["linux", "darwin"] :
        sqlite_path="/"+sqlite_path
        tinydb_path="/"+tinydb_path
        db_base_path="/"+db_base_path

    else:
        sqlite_path="Unknown system platform (" + sys.platform + "). Please set sqlite connection string yourself accordingly"
    
    cookie_secret = uuid.uuid4()

    for dirname, dirs, files in os.walk(root):
        for f in files:
            # skipping the exclude_files in update_only mode
            if not (f in exclude_files and update_only):
                print(" processing: " + f)
                print("  in: " + dirname)
                path=Path(dirname)
                index = path.parts.index("start")
                opath = Path(outdir).joinpath(*path.parts[index+1:])
                print("  out: " + str(opath))
                filename, file_extension = os.path.splitext(f)
                print("  filename: " + filename)
                print("  file ext: " + file_extension)
                print("  path.parts-1: " + path.parts[-1])
                if path.parts[-1] in skip_dirs:
                    print("skipped: " + str(f))    
                else:
                    if not os.path.exists(str(opath)):
                        os.makedirs(str(opath), exist_ok=True)
                    if (file_extension in template_exts) and not (path.parts[-1] in exclude_dirs):
                            copy_or_pump(
                                os.path.normpath(os.path.join(dirname, f)),
                                os.path.normpath(os.path.join(str(opath), f)),
                                copy=False,
                                appname=appname,
                                sqlite_path=sqlite_path,
                                tinydb_path=tinydb_path,
                                db_base_path=db_base_path,
                                dbtype=dbtype,
                                cookie_secret=str(cookie_secret),
                                data="""{{data}}""",
                                force=force
                                )
                    else:
                        copy_or_pump(
                            os.path.normpath(os.path.join(dirname, f)),
                            os.path.normpath(os.path.join(str(opath), f)),
                            copy=True,
                            appname=appname,
                            sqlite_path=sqlite_path,
                            tinydb_path=tinydb_path,
                            db_base_path=db_base_path,
                            dbtype=dbtype,
                            cookie_secret=str(cookie_secret),
                            data="""{{data}}""",
                            force=force
                            )
            else:
                print("skipped in update_only: " + str(f))
    print(" DB path: " + sqlite_path)
    #
    # rename the view file extension according the --view paramter
    #
    if view_type:
        print(50*"-")
        if view_type == "bs4":
            print("preparing app for view_type: Bootstrap 4")
        elif view_type == "sui":
            print("preparing app for view_type: SemanticUI ")
        else:
            print("preparing app for view_type: " + str(view_type))
        print(50*"-")
        if view_type == "bs4":
            folder = os.path.normpath(os.path.join( outdir, "views"))
            #rename_extensions(folder, ".tmpl", ".bs4")
            rename_extensions(folder, "." + view_type, ".tmpl", files=["index", "error", "404"])
            print("   ... Done. Bootstrap4 is the default")
            # nothing else to do since everything is already prepared for bs4 (default)
        else:
            # for all others the trick is to 
            # 1. rename all .tmpl to .bs4 (default)
            # 2. rename all .view_type to .tmpl
            print("outdir: " + outdir)
            import os,sys
            folder = os.path.normpath(os.path.join( outdir, "views"))
            #rename_extensions(folder, ".tmpl", ".bs4")
            rename_extensions(folder, "." + view_type, ".tmpl",  files=["index", "error", "404"])
    else:
        print("Error: viewtype not set and apparantly no Default set either!")
    
    if update_only:
        print(40*"-")
        print("   Update only. ")
        print(40*"-")
        print( "  I did not touch:  ")
        print(exclude_files)
        print(skip_dirs)

def rename_extensions(folder, old_ext, new_ext, files=None):
    """
        renames all file extension in the givben folder 
        from *.old_ext to *.new_ext
    """
    for filename in os.listdir(folder):
        infilename = os.path.join(folder,filename)
        # rename all file extensions
        if not os.path.isfile(infilename): continue
        oldbase, ext = os.path.splitext(filename)
        if files and oldbase not in files: continue
        #print("   ...   found a: " + str(ext) + " file")
        if not ext == old_ext: continue
        #newname = infilename.replace( old_ext, + new_ext)
        newname = os.path.join(folder, oldbase + new_ext)
        print("   ... renaming: " + infilename + " -> " + newname)
        #output = os.rename(infilename, newname)
        output = shutil.move(infilename, newname)
    return

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', "--name", action="store", 
        dest="name", help='-n appname',
        required=True)

    parser.add_argument('-p', "--path", action="store", 
        dest="path", help='-p out_path', default="..",
        required=False)

    parser.add_argument("-f", "--force", 
        action="store_true", dest="force", default=False,
        help="force overwriting if invoked on existing app [default]")

    parser.add_argument("-u", "--update", 
        action="store_true", dest="update_only", default=False,
        help="Only update the Pow parts. Excludes your changes to models, config etc.")

    parser.add_argument("-t", "--type", 
        action="store", dest="view_type", default="bs4",
        help="set the default view framework. (semanticui = sui || bootstrap 4 = bs4 (default))")
    #
    # db type
    # 
    #parser.add_argument('-d', "--db", action="store", 
    #                    dest="db", help='-d which_db (mongo || tiny || peewee_sqlite) default = sql',
    #                    default="sql", required=False)
    
    
    
    args = parser.parse_args()
    #
    # show some args
    #
    #print("all args: ", args)
    #print(dir(args))
    #print("pluralized model name: ", pluralize(args.name))
   

    print(50*"-")
    print(" Generating your app: " + args.name)
    print(50*"-")
    #generate_app(args.name, args.force, args.path, dbtype=args.db, update_only=args.update_only)
    generate_app(args.name, force=args.force, outpath=args.path, update_only=args.update_only, view_type=args.view_type)

    base = os.path.normpath(os.path.join(os.getcwd(), args.path))
    apppath = os.path.normpath(os.path.join(base, args.name))
    tpath = os.path.normpath(os.path.join(base, "migrations"))
    # create the versions directory
    os.makedirs(os.path.normpath(os.path.join(tpath, "versions")), exist_ok=True)
    # create the views directory
    #os.makedirs(os.path.normpath(os.path.join(base, "migrations")), exist_ok=True)
    print()
    #print(50*"-")
    if args.update_only:
        print(50*"-")
        print(" UPDATED YOUR APP!!!")
        print(50*"-")
        print(" Successfully updated your application")   
        sys.exit()
    else:
        print(" Successfully created your application")
    print()
    print(50*"-")
    print("Your next steps: ")
    print("  1. [Optional step: create a virtualenv in you app directory]")
    print("      virtualenv " + apppath )
    print("  2. cd to you new apps directory: " + apppath)
    print("     [optionally activate the virtualenv]")
    print("  3. pip install -r requirements.txt")
    print("  4. run: python server.py")
    print("  5. open your browser with http://localhost:8080")
    print(50*"-")
    print()
    print(50*"-")
    print("Remark:")
    print("  You can move your app subdir to wherever you want")
    print("  as long as its on the pythonpath")
    print("  Windows: set PYTHONPATH=%PYTHONPATH%;"+base)
    print("  linux/osx: export PYTHONPATH=$PYTHONPATH:"+base)
    print(50*"-")
    print()

if __name__ == "__main__":
    main()