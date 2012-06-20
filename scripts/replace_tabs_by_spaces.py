import sys,os,os.path
import string


if __name__ == "__main__":

    
    for (path, dirs, files) in os.walk("../"):
        print path
        for file in files:
            if not path.find(".git"):
                print "process", path + file
                infile = os.path.join(path, file)
                f = open(infile,"r")
                out = ""
                
                for line in f.readlines():
                    out += line.replace("\t", "    ")
                f.close()
                os.remove(infile)
                outfile = open(infile, "w")
                outfile.write(out)
                outfile.close()
            
    sys.exit(0)