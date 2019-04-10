#
# super simple ci/cd with invoke ;)
# 
# invoke docs = http://docs.pyinvoke.org/en/1.2/getting-started.html
#       specific: change workdir: https://github.com/pyinvoke/invoke/issues/225

from invoke import task
import os,sys

@task
def build(c, path="../..", name="testapp"):
    """
        Create a testapp from the current git version
            generate_app -n <name> -p <path>
        create the according venv
            cd (abspath)
            virtrualenv venv
        activate the pip environment
            win: venv\Scripts\activate
            other: source venv/bin/activate
        install the requirements
            pip install -r requirements.txt
        run the tests
            cd tests
            python runtests
        run the server
            python server.py
        
        => You can find the testresults here:
            localhost:8080/testresults
    """
    if not os.name in ["nt", "posix"]:
        print("Sorry. this only supports Posix (e.g. Linux, OSX) and Windows OS. ")
        sys.exit()

    path=os.path.normpath(path)
    print("Building : -n {} -p {} ".format(name, path))
    if os.path.exists(os.path.join(path, name)):
        print("sorry, path / name exists")
        r=input(" .. type y or yes, to go ahead deleting the existing: {} ?".format(os.path.join(path,name)))
        if r in ["y", "yes"]:
            import shutil
            r=shutil.rmtree(os.path.join(path,name))
            print(40*"-")
            print(" ..... deleted dir tree: {}".format(os.path.join(path, name)))
            print(40*"-")
            build_all(c,name, path)
        else:
            print(40*"-")
            print(" ok, exiting...")
            print(40*"-")
            sys.exit()
    else:
        # start the build and check
        build_all(c,name, path)

def build_all(c,name, path, force=False):
    """
        the actual function that does the job
    """
    print(40*"-")
    print(" starting the build and check...")
    print(40*"-")
    # genate the app
    if force:
        r=c.run("python generate_app.py -n {} -p {} -f".format(name, path))
    else:
        r=c.run("python generate_app.py -n {} -p {}".format(name, path))
        
    print(" .. generated the PythonOnWheels app.")
    # switch the current dir for invoke. every c.run starts from that dir.
    app_path=os.path.abspath(os.path.join(path, name))
    with c.cd(app_path):
        # create a venv
        if os.name == "nt":
            print(" .. creating a virtualenv")
            c.run("virtualenv ./venv")
            print(" .. Installing the PoW requirements")
            c.run("cd ./venv/Scripts && pip.exe install -r {}".format(
                os.path.normpath(os.path.join("..\..", "requirements.txt"))))
    test(c,path,name)
    runserver(c,path,name)

@task
def test(c,  path="../..", name="testapp"):
    path=os.path.normpath(path)
    app_path=os.path.abspath(os.path.join(path, name))
    print("app_path: " + app_path)
    with c.cd(os.path.join(app_path, "tests")):
        print("cwd: " + c.cwd)
        print(" .. running the tests .. ")
        pypath=os.path.normpath(os.path.join(app_path,"./venv/Scripts/python.exe"))
        print("pyhton.exe path:" + pypath)
        c.run("{} runtests.py".format(pypath))

@task
def runserver(c, path="../..", name="testapp"):
    path=os.path.normpath(path)
    app_path=os.path.abspath(os.path.join(path, name))
    print("app_path: " + app_path)
    with c.cd(app_path):
        print(" .. starting the server .. ")
        print(" .. check testresults at: localhost:8080/testresults")
        pypath=os.path.normpath(os.path.join(app_path,"./venv/Scripts/python.exe"))
        c.run("{} server.py".format(pypath))
        

@task
def clean(c, path="../..", name="testapp", force=False):
    app_path=os.path.abspath(os.path.normpath(os.path.join(path,name)))
    r=input(" deleting the existing: {} ? Type: y | yes: ".format(app_path))
    if r in ["y", "yes"]:
        import shutil
        r=shutil.rmtree(os.path.join(path,name))
        print(40*"-")
        print(" ..... deleted dir tree: {}".format(app_path))
        print(40*"-")

    
