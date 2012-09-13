#
# kill all those ugly tabs ( \t ) and replace it with 4-spaces
#
#


import sys
import os
import os.path

exclude_dirs = [".git"]
if __name__ == "__main__":
    path = "./"
    i = 0
    for (path, dirs, files) in os.walk(path):
        for elem in exclude_dirs:
            #print "comparing:", path , " with:", elem, "result:", path.find(elem)
            if path.find(elem) < 0:
                print "path: ", path
                print "dirs: ",dirs
                print "files: ",files
                for item in files:
                    (name, ext) = os.path.splitext(item)
                    print "%-20s ==> %10s" % (name, ext)
                print "----"
            else:
                print "excluding: ", path 
        
        i += 1
        if i >= 3:
            break