#!C:\Python26\python.exe -u

#  pow model generator.
#
# options are: 
#    no option or -create         means create
#    -remove             removes 

from optparse import OptionParser
import sqlite3, sys, os, datetime
import string
import generate_migration

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models/powmodels" )))
import powlib


# setting the right defaults
MODE_CREATE = 1
MODE_REMOVE = 0

pow_newline = powlib.linesep
pow_tab= powlib.tab

def main():
    parser = OptionParser()
    mode= MODE_CREATE
    parser.add_option("-n", "--name",  action="store", type="string", dest="name", help="creates model named model-name", default ="None")
    parser.add_option("-a", "--attributes",  action="store", type="string", dest="actions", help="defines the attributes included in the model.", default ="None")
    parser.add_option("-f", "--force",  action="store_true",  dest="force", help="forces overrides of existing files",default="False")
    parser.add_option("-c", "--comment",  action="store", type="string", dest="comment", help="defines a comment for this migration.", default ="No Comment")
    #parser.add_option("-n", "--no-migration",  action="store_true",  dest="nomig", help="supress creation of the related migration for this model",default="False")    
    
    
    (options, args) = parser.parse_args()
    #print options
    if options.name == "None":
        parser.error("You must at least specify a modelname by giving -n <name>.")
        return
    else:
        model_dir = os.path.normpath("./models/")
        modelname = options.name
        start = None
        end = None
        start = datetime.datetime.now()
        
        render_model(modelname, options.force, options.comment)
        
        end = datetime.datetime.now()
        duration = None
        duration = end - start 
        print "generated_model in("+ str(duration) +")"
        return

    
def render_model(modelname, force, comment, properties=None):
    
    print "generate_model: " + modelname
    #print "force: ", force
    infile = None
    infile = open (os.path.normpath("./stubs/can_be_edited.txt"), "r")
    ostr = infile.read()
    infile.close()
    
    # add a creation date
    ostr = ostr + pow_newline
    ostr = ostr + "# date created: \t" + str(datetime.date.today())
    ostr = ostr + pow_newline
    
    # Add the model_stub content to the newly generated file. 
    infile = open (os.path.normpath("./stubs/model_stub_part1.py"), "r")
    ostr = ostr + infile.read()
    infile.close()
    classname = string.capitalize(modelname)  
    baseclassname = "Base" + classname
    
    ostr += "import " + baseclassname + powlib.newline
    ostr += powlib.newline
    #ostr += "import " + baseclassname + powlib.linesep + powlib.linesep
    ostr += render_class(classname, baseclassname + "." + baseclassname)
    ostr += powlib.tab + "pass" + powlib.newline
        
    # write the output file to disk
    filename = classname + ".py"
    filename = os.path.normpath( "./models/" + filename)
    file_exists = False
    if os.path.isfile( os.path.normpath(  filename) ):
        file_exists = True
    else:
        file_exists = False
    if file_exists and force != True:
        print filename + " (exists)...(Use -f to force override)"
    else:
        ofile = open(  filename , "w+") 
        print " --", filename + " (created)"
        ofile.write( ostr )
        ofile.close()
    ### genrate BaseModel if neccessary
    filename = "Base" + classname + ".py"
    
    ### generate the BaseClass
    infile = None
    infile = open (os.path.normpath("./stubs/basemodel_stub_part0.py"), "r")
    ostr = infile.read()
    infile.close()
    
    ostr += "class " + baseclassname +"(Base):" + powlib.newline
    infile = open (os.path.normpath("./stubs/basemodel_stub_part1.py"), "r")
    ostr += infile.read()
    infile.close()
    ostr += powlib.tab + "__table__ = Base.metadata.tables['" + powlib.plural(string.lower(modelname)) +"']" 
    ostr += powlib.newline
    infile = open (os.path.normpath("./stubs/basemodel_stub_part2.py"), "r")
    ostr += infile.read()
    infile.close()
    ### adding the properties list
    if properties == None:
        ostr += powlib.tab + "properties_list = []" + powlib.newline
    else:
        ostr += powlib.tab + "properties_list = " + properties  + powlib.newline
    ostr += powlib.tab + "modelname = '" + string.capitalize(modelname) + "'" + powlib.newline
    infile = open (os.path.normpath("./stubs/basemodel_stub_part3.py"), "r")
    ostr += infile.read()
    infile.close()
        
        
    filename = os.path.normpath( "./models/basemodels/" + filename)
    if os.path.isfile( os.path.normpath(  filename) ) and force != True:
        print filename + " (exists)...(Use -f to force override)"
    else:
        ofile = open(  filename , "w+") 
        print  " --", filename + " (created)"
        ofile.write( ostr )
        ofile.close()
        
    # check if App / BaseApp exist and repair if necessary
    if os.path.isfile(os.path.normpath( "./models/basemodels/BaseApp.py")):
        #BasApp exists, ok.
        pass
    else:
        # copy the BaseClass
        powlib.check_copy_file(os.path.normpath( "./stubs/BaseApp.py"), os.path.normpath( "./models/basemodels/"))
        
    if os.path.isfile(os.path.normpath( "./models/powmodels/App.py")):
        #App exists, ok.
        pass
    else:
        # copy the BaseClass
        powlib.check_copy_file(os.path.normpath( "./stubs/App.py"), os.path.normpath( "./models/powmodels/"))
        
    render_test_stub(modelname, classname)
    return 

def reset_model(modelname):
    return render_model(modelname, True, "", properties=None, nomig=True)
    
def render_test_stub (modelname, classname ):
    #print "rendering Testcase for:", classname, " ", " ", modelname
    print " -- generating TestCase...",
    infile = open( os.path.normpath("./stubs/test_model_stub.py"), "r")
    ofile = open( os.path.normpath("./tests/models/Test"+classname+".py"), "w")
    instr = infile.read()
    instr = instr.replace("#CLASSNAME", classname)
    ofile.write(instr)
    infile.close()
    ofile.close()
    print " ..(created)"
    
    
    
    return

def render_method( name, vars=[], body = []):
    #
    # call with
    #     name: method name
    #     vars = [ ("var1","None"), ("var2","1"), ... ]
    #
    ostr = ""
    ostr += pow_tab + "#" + pow_newline
    ostr += pow_tab + "# Method: " + name  + pow_newline
    ostr += pow_tab + "#" + pow_newline
    
    if len(vars) == 0:
        ostr = ostr + pow_tab + "def " + name + "(self):" + pow_newline
    else:
        ostr = ostr + pow_tab + "def " + name + "(self"
        for var,val  in vars:
            if val == None:
                str = ostr + "," + str(var)
            else:
                str = ostr + "," + str(var) + "=" +str(val)
        ostr = ostr + "):" + pow_newline
    #
    # mehtod body
    #
    if body == []:
        ostr = ostr + pow_tab + pow_tab + "pass" + pow_newline
    else:
        for elem in body:
            ostr += pow_tab + pow_tab  + elem+ powlib.linesep
        
    ostr += pow_newline
    #print ostr
    return ostr

def render_class( classname, baseclass="object"):
    #
    # call with    name: class name
    #
    ostr = ""
    ostr += "class " + classname + "(" + baseclass + "):" + pow_newline
    
    ostr += pow_tab + "#" + pow_newline
    ostr += pow_tab + "# Class: " + classname  + pow_newline
    ostr += pow_tab + "#" + pow_newline
    #ostr += pow_newline
    #print ostr
    
    return ostr
    
    
if __name__ == '__main__':
    main()
