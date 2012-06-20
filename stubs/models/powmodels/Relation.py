import sys,os

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../basemodels" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../basemodels/pow" )))
import powlib

import BaseRelation

class Relation(BaseRelation.BaseRelation):
	pass

