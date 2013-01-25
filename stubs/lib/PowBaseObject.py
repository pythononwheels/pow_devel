import sys, datetime, os, getopt, shutil
import ConfigParser,string
import re

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.normpath("../config/"))
import powlib
import db
import pow


class PowBaseObject(object):
    """ pow base object class"""
    #__engine__= create_engine(powlib.get_db_conn_str("../config/"))
    __engine__= None
    __metadata__ = MetaData(bind = __engine__)
    __session__ = sessionmaker(bind = __engine__)
    
    def __init__(self):
        #env = pow.global_conf["ENV"]
        logging = pow.logging["SQLALCHEMY_LOGGING"]
        if logging == "True":
            PowBaseObject.__engine__= create_engine(powlib.get_db_conn_str(), echo = True)
        else:
            PowBaseObject.__engine__= create_engine(powlib.get_db_conn_str(), echo = False)
        PowBaseObject.__metadata__.bind =  PowBaseObject.__engine__
        PowBaseObject.__session__.configure( bind = PowBaseObject.__engine__ )
        
    def dispatch(self):
        print "object:" + str(self) +  "dispatch() method invoked"
        return
    
    def getMetaData(self):
        return PowBaseObject.__metadata__
    
    def getEngine(self):
        return PowBaseObject.__engine__
    
    def getSession(self):
        return PowBaseObject.__session__()
        
    def getConnection(self):
        return PowBaseObject.__engine__.connect()
        
    def repr(self):
        return "Not implemented in class: PowBaseObject"