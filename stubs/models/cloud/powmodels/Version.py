import sys,os

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../basemodels" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../basemodels/pow" )))
import powlib

import BaseVersion

class Version(BaseVersion.BaseVersion):
    def __init__(self):
        #print "__init__ was called on App"
        BaseVersion.BaseVersion.__init__(self)

    def __new__(klass, *args, **kwargs):
        #print "__new__ was called on %s" % str(klass)
        return super(Version, klass).__new__(klass, *args, **kwargs)
