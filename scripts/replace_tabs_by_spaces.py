import sys,os,os.path
import string


if __name__ == "__main__":

    exclude_dirs=["git"]
    for (path, dirs, files) in os.walk("../"):
        for file in files:
            print path
            if "git" in path or "scripts" in path:
                print "skip ", path
            else:
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
    