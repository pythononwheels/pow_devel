from {{appname}}.models.sql.basemodel import SqlBaseModel
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql.expression import func 

class SqlModel(SqlBaseModel):
    """
        This is the basic class for extensions to put their code
        which is relevant for all models of this type.abs

        Hierarchy: 
         scope:         all         db specific       db specific free
         control:       pow             pow             user/extension
                    modelobject ->    (SQL)basemodel      ->  sqlmodel
    """
    #id =  Column(Integer, primary_key=True)
    #created_at = Column(DateTime, default=func.now())
    #last_updated = Column(DateTime, onupdate=func.now(), default=func.now())