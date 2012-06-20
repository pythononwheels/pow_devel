
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from sqlalchemy.sql import delete
#import migrate.changeset
#from migrate.changeset.constraint import ForeignKeyConstraint
from sqlalchemy.schema import CreateTable
from sqlalchemy import event, DDL

import sys,os,datetime
import string
import types
import urllib

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../powmodels" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../" )))
import powlib
from PowBaseObject import PowBaseObject
from PowAppObject import PowAppObject
import Relation
import generate_model

x = PowBaseObject()
y = PowAppObject()
Base = declarative_base(bind=x.__engine__, metadata = x.__metadata__)
Base.metadata.reflect()

