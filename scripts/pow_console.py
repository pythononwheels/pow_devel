#!python
## Thx to:
##  http://code.activestate.com/recipes/355319/ (r1)
## eased my life. Console and the  recipe above ;)
import code
import sys,os, string
try:
  import pyreadline as readline
except ImportError:
  import readline

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))

class FileCacher:
    "Cache the stdout text so we can analyze it before returning it"
    def __init__(self): self.reset()
    def reset(self): self.out = []
    def write(self,line): self.out.append(line)
    def flush(self):
        output = '\n'.join(self.out)
        self.reset()
        return output

class Shell(code.InteractiveConsole):
    "Wrapper around Python that can filter input/output to the shell"
    def __init__(self):
        self.stdout = sys.stdout
        self.cache = FileCacher()
        code.InteractiveConsole.__init__(self)
        # importing the pow modules as well as 
        # current Models, Controllers for this project
        importdirs = ["models/basemodels", "models", "controllers" ]
        include_ext_list = [".py"]
        for adir in importdirs:
            sys.path.append(os.path.abspath(adir))
            
        for path in importdirs:
            importlist = []
            for elem in os.listdir(os.path.normpath(path)):
                fname, fext = os.path.splitext(elem)
                if fext in include_ext_list:
                    statement = "from "+ str(fname)+ " import " + str(fname)
                    print "executing statement: ", statement
                    #exec statement
                    self.push(statement)
        return
    
    def get_output(self): sys.stdout = self.cache
    def return_output(self): sys.stdout = self.stdout

    def push(self,line):
        self.get_output()
        # you can filter input here by doing something like
        #print "hey, this is the input: ", line
        # line = filter(line)
        newline = line
        code.InteractiveConsole.push(self,newline)
        self.return_output()
        output = self.cache.flush()
        # you can filter the output here by doing something like
        # output = filter(output)
        if output != "":
            print output # or do something else with it
        return 

if __name__ == '__main__':
    sh = Shell()
    
    pow_banner = "pow console v0.1 " + os.linesep
    pow_banner += "Using python " + str(sys.version)[:6] + os.linesep
    pow_banner += "type help to get more info and help on special pow_console commands"
     
    sh.interact(pow_banner)
## end of http://code.activestate.com/recipes/355319/ }}}
