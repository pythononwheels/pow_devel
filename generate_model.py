#!python
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
    """ Executes the render methods to generate a model, basemodel and basic tests according to the given options """
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
    """
    Renders the generated Model Class in prefix_path/models.
    Renders the according BaseModel in prefix_path/models/basemodels.
    Renders a basic test in tests dierctory.
    Uses the stubs from stubs/partials.
    """
    print "generate_model: " + modelname
    # new model filename
    classname = string.capitalize(modelname)  
    baseclassname = "Base" + classname
    filename = classname + ".py"
    filename = os.path.normpath( prefix_path+ "/models/" + filename)
    if os.path.isfile( os.path.normpath( filename ) ) and force != True:
        print filename + " (exists)...(Use -f to force override)"
    else:
        infile = None
        infile = open (os.path.normpath( PARTS_DIR +  "model_stub.py"), "r")
        ostr = ""
        ostr = ostr + infile.read()
        infile.close()
        
        ostr = ostr.replace("#DATE", str(datetime.date.today()) )
        ostr = ostr.replace("#MODELCLASS", classname)
        
        ostr = ostr.replace("#BASECLASS", baseclassname)
   
        # write the output file to disk
        ofile = open( filename , "w+") 
        print " --", filename + " (created)"
        ofile.write( ostr )
        ofile.close()
    
    ### generate BaseModel if neccessary
    filename = "Base" + classname + ".py"
    if os.path.isfile( os.path.normpath( filename ) ) and force != True:
        print filename + " (exists)...(Use -f to force override)"
    else:
        infile = None
        ### generate the BaseClass
        infile = open (os.path.normpath( PARTS_DIR +  "basemodel_stub.py"), "r")
        ostr = infile.read()
        infile.close()
        # Add Class declaration and Table relation for sqlalchemy
        ostr = ostr.replace("#MODELCLASS",  baseclassname )
        ostr = ostr.replace( "#MODELTABLE",  powlib.plural(string.lower(modelname))  ) 
         
        ### adding the properties list
        # TODO: Needs to be tested. 
        if properties == None:
            ostr = ostr.replace("#PROPERTIES_LIST",  "[]")
        else:
            ostr = ostr.replace("#PROPERTIES_LIST",  "[" + properties + "]")
            
        ostr = ostr.replace("#MODELNAME" , string.capitalize(modelname) )        
            
        filename = os.path.normpath( prefix_path + "/models/basemodels/" + filename)
    
        ofile = open(  filename , "w+") 
        print  " --", filename + " (created)"
        ofile.write( ostr )
        ofile.close()
        
    # render a basic testcase 
    render_test_stub(modelname, classname, prefix_path, PARTS_DIR)
    return 

def reset_model(modelname):
    """ overwrites the generated Model, BaseModel and Test with empty / newly generated versions."""
    return render_model(modelname, True, "", properties=None, nomig=True)
    
def render_test_stub (modelname, classname, prefix_path = "", PARTS_DIR = powlib.PARTS_DIR ):
    """ renders the basic testcase for a PoW Model """
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


    
if __name__ == '__main__':
    main()
