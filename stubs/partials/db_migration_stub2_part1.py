
from sqlalchemy import *
from sqlalchemy.schema import CreateTable
from sqlalchemy import event, DDL

import sys
import os

sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../models" )))
sys.path.append( os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), "../lib" )))

import powlib
from PowTable import PowTable
from BaseMigration import BaseMigration

class Migration(BaseMigration):
