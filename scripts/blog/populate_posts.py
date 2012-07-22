#
# read bram stoker dracula and make a blog post
# from every chapters first 200 words
#
import sys, string

sys.path.append("../models/")

import Post

if __name__=="__main__":
    f = open("../public/doc/dracula.txt","r")
    counter = 0
    found = False
    postlist = []
    l = [l for l in f.readlines() if l.strip()]
    #print l
    skip = 0
    for line in l:
        counter += 1
        if line.lower().find("chapter") != -1 and skip <= counter:
            print line
            p = Post.Post()
            p.title = l[counter]
            p.content = ""
            content = l[counter+1:counter+20]
            #print content
            for elem in content:
                elem = elem.replace("\n","<br>")
                elem = elem.replace("\r\n","<br>")
                p.content += elem
                #print elem
            skip = counter+3
            p.create()
            print p
    sys.exit(0)