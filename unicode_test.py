# unicode test for BasePost
# 
import sys, os

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "./models/basemodels" )))


import BasePost
import Post

if __name__ == "__main__":
    b = BasePost.BasePost()
    
    s_title = "Hällo"
    unicode_title = s_title.decode("utf-8")
    print s_title, type(s_title)
    print unicode_title, type(unicode_title)
    b.title = unicode_title
    b.utitle = unicode_title
    b.strtitle = unicode_title
    #print b.title, type(b.title)
    b.create()
    