#!C:\Python26\python.exe -u

#  pow model generator.
#
# options are: 
#    see python generate_model.py --help

from optparse import OptionParser
import sqlite3, sys, os, datetime
import string

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models/powmodels" )))
import powlib


# setting the right defaults
MODE_CREATE = 1
MODE_REMOVE = 0
PARTS_DIR = powlib.PARTS_DIR
MODEL_TEST_DIR = "/tests/models/" 
pow_newline = powlib.linesep
pow_tab= powlib.tab

def main():
    parser = OptionParser()
    mode= MODE_CREATE
    parser.add_option("-n", "--name",  action="store", type="string", dest="name", help="creates model named model-name", default ="None")
    parser.add_option("-a", "--attributes",  action="store", type="string", dest="actions", help="defines the attributes included in the model.", default ="None")
    parser.add_option("-f", "--force",  action="store_true",  dest="force", help="forces overrides of existing files",default="False")
    parser.add_option("-c", "--comment",  action="store", type="string", dest="comment", help="defines a comment for this model.", default ="No Comment")
    parser.add_option("-p", "--path",  action="store", type="string", dest="path", help="sets the model output psth.", default ="./")
    #parser.add_option("-n", "--no-migration",  action="store_true",  dest="nomig", help="supress creation of the related migration for this model",default="False")    
    
    
    (options, args) = parser.parse_args()
    #print options
    if options.name == "None":
       if len(args) > 0:
           # if no option flag (like -n) is given, it is assumed that the first argument is the model name. (representing -n arg1)
           options.name = args[0]
       else:
           parser.error("You must at least specify an appname by giving -n <name>.")

    #model_dir = os.path.normpath("./models/")
    model_dir = os.path.normpath(options.path)
    modelname = options.name
    start = None
    end = None
    start = datetime.datetime.now()
    
    render_model(modelname, options.force, options.comment, model_dir)
    
    end = datetime.datetime.now()
    duration = None
    duration = end - start 
    print "generated_model in("+ str(duration) +")"
    return

    
def render_model(modelname, force, comment, prefix_path="./", properties=None, PARTS_DIR = powlib.PARTS_DIR ):
    
    print "generate_model: " + modelname
    #print "force: ", force
    infile = None
    infile = open (os.path.normpath( PARTS_DIR + "can_be_edited.txt"), "r")
    ostr = infile.read()
    infile.close()
    
    # add a creation date
    ostr = ostr + pow_newline
    ostr = ostr + "# date created: \t" + str(datetime.date.today())
    ostr = ostr + pow_newline
    
    # Add the model_stub content to the newly generated file. 
    infile = open (os.path.normpath( PARTS_DIR +  "model_stub_part1.py"), "r")
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
    filename = os.path.normpath( prefix_path+ "/models/" + filename)
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
    infile = open (os.path.normpath( PARTS_DIR +  "basemodel_stub_part0.py"), "r")
    ostr = infile.read()
    infile.close()
    
    ostr += "class " + baseclassname +"(Base):" + powlib.newline
    infile = open (os.path.normpath( PARTS_DIR +  "basemodel_stub_part1.py"), "r")
    ostr += infile.read()
    infile.close()
    ostr += powlib.tab + "__table__ = Base.metadata.tables['" + powlib.plural(string.lower(modelname)) +"']" 
    ostr += powlib.newline
    infile = open (os.path.normpath( PARTS_DIR +  "basemodel_stub_part2.py"), "r")
    ostr += infile.read()
    infile.close()
    ### adding the properties list
    if properties == None:
        ostr += powlib.tab + "properties_list = []" + powlib.newline
    else:
        ostr += powlib.tab + "properties_list = " + properties  + powlib.newline
    ostr += powlib.tab + "modelname = '" + string.capitalize(modelname) + "'" + powlib.newline
    infile = open (os.path.normpath( PARTS_DIR +  "basemodel_stub_part3.py"), "r")
    ostr += infile.read()
    infile.close()
        
        
    filename = os.path.normpath( prefix_path + "/models/basemodels/" + filename)
    if os.path.isfile( os.path.normpath(  filename) ) and force != True:
        print filename + " (exists)...(Use -f to force override)"
    else:
        ofile = open(  filename , "w+") 
        print  " --", filename + " (created)"
        ofile.write( ostr )
        ofile.close()
        
    # check if App / BaseApp exist and repair if necessary
    #if os.path.isfile(os.path.normpath( "./models/basemodels/BaseApp.py")):
    #    #BasApp exists, ok.
    #    pass
    #else:
    #    # copy the BaseClass
    #    powlib.check_copy_file(os.path.normpath(  PARTS_DIR +  "BaseApp.py"), os.path.normpath( "./models/basemodels/"))
        
    #if os.path.isfile(os.path.normpath( "./models/powmodels/App.py")):
    #    #App exists, ok.
    #    pass
    #else:
    #    # copy the BaseClass
    #    powlib.check_copy_file(os.path.normpath( PARTS_DIR +  "App.py"), os.path.normpath( "./models/powmodels/"))
        
    render_test_stub(modelname, classname, prefix_path, PARTS_DIR)
    return 

def reset_model(modelname):
    return render_model(modelname, True, "", properties=None, nomig=True)
    
def render_test_stub (modelname, classname, prefix_path = "", PARTS_DIR = powlib.PARTS_DIR ):
    #print "rendering Testcase for:", classname, " ", " ", modelname
    print " -- generating TestCase...",
    infile = open( os.path.normpath( PARTS_DIR +  "test_model_stub.py"), "r")
    test_name = "Test" + classname + ".py"
    ofile = open( os.path.normpath(prefix_path + MODEL_TEST_DIR + test_name ), "w")
    instr = infile.read()
    instr = instr.replace("#CLASSNAME", "Test" +  classname )
    ofile.write(instr)
    infile.close()
    ofile.close()
    print  " %s...(created)" % (prefix_path + MODEL_TEST_DIR + test_name)
    
    return


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
