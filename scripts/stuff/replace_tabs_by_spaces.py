import sys,os,os.path
import string
     
if __name__ == "__main__":

    
    for (path, dirs, files) in os.walk("../"):
        print path
        for file in files:
            if "git" in path or "scripts" in path:
                #print "skipping: ", path
                pass
            else:
                filename, extension = os.path.splitext(file)
                #print filename, "  ", extension
                if extension ==".py":
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