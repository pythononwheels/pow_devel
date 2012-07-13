
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

# the libraries
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../lib" )))
# the models
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../" )))
# the generators
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../../" )))

import powlib
from PowBaseObject import PowBaseObject

import generate_model

x = PowBaseObject()

Base = declarative_base(bind=x.__engine__, metadata = x.__metadata__)
Base.metadata.reflect()

