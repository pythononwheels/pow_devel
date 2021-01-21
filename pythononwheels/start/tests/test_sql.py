#
# Pow Default Tests
# 
#
# runtest script.
# runs test with respect to some paramters
# currently only os 

import sys
import pytest
import time
# possible sys.platform results:
# http://stackoverflow.com/questions/446209/possible-values-from-sys-platform


#
# SQL tests 
#
@pytest.mark.run(order=1)
@pytest.mark.minimal
def test_sql_generate_model(modelname):
    """ test if sql model is generated"""
    print(" .. Test generate_model")
    import {{appname}}.generate_model as gm
    import uuid
    import os.path
    ret = gm.generate_model(modelname, "sql", appname="{{appname}}")
    # generate model returns true in case of success
    assert ret is True
    assert os.path.exists(os.path.normpath("../models/sql/" + modelname + ".py"))

@pytest.mark.run(order=2)
@pytest.mark.minimal
def test_sql_model_type():
    """ based on test_generate_model. Tests if a model can insert values 
        DB sqlite by default.
    """ 
    print(" .. Test if SQL model is correct type")
    from {{appname}}.models.sql.pow_test_model import PowTestModel
    m = PowTestModel()
    assert isinstance(m, PowTestModel)

@pytest.mark.run(order=3)
def test_sql_dbsetup():
    """ test the setup of the alembic environment """
    print(" .. Test SQL: db_setup")
    import {{appname}}.init_sqldb_environment
    import os
    os.chdir("..")
    r = {{appname}}.init_sqldb_environment.init_migrations()
    assert r == True
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

@pytest.mark.run(order=4)
def test_sql_migration():
    """ test the setup of the alembic environment 
        generate a migration
    """
    print(" .. Test SQL: generate_migration")
    import {{appname}}.generate_migration
    import os
    os.chdir("..")
    script = {{appname}}.generate_migration.generate_migration(message="pow_test")
    assert os.path.exists(os.path.normpath(script.path))
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

@pytest.mark.run(order=5)
def test_sql_dbupdate():
    """ test the setup of the alembic environment 
        actually migrate the DB schema up
    """
    print(" .. Test SQL: update_db -d up")
    import {{appname}}.update_db
    import os, time
    ret = None
    os.chdir("..")
    time.sleep(1)
    try:
        ret = {{appname}}.update_db.migrate("up")
    except Exception as e:
        print(e)
        ret = True
    time.sleep(5)
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

@pytest.mark.run(order=6)
def test_if_sql_model_validation_works():
    """ 
        check if validation works
    """ 
    print(" .. Test SQL: model.upsert() and model.find()")
    from {{appname}}.models.sql.pow_test_model import PowTestModel
    m = PowTestModel()
    assert m.validate() == True

@pytest.mark.run(order=7)
def test_if_sql_model_validation_fails_successfully():
    """ 
        check if validation fails if type is wrong
    """ 
    print(" .. Test SQL: model.upsert() and model.find()")
    from {{appname}}.models.sql.pow_test_model import PowTestModel
    m = PowTestModel()
    m.title="123456789123456789123456789123456789"
    assert m.validate() == False

@pytest.mark.run(order=8)
def test_sql_insert_and_find():
    """ based on test_generate_model. 
        Tests if a model can insert values in the DB 
        and can be found by title attribute.
    """ 
    print(" .. Test SQL: model.upsert() and model.find()")
    from {{appname}}.models.sql.pow_test_model import PowTestModel
    import os
    m = PowTestModel()
    m.title = "TestnamePowTestRunner"
    m.upsert()
    res=m.find(PowTestModel.title=="TestnamePowTestRunner")
    assert res.count()==1
    m.session.close()
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    
if __name__ == "__main__":
    
    print(55*"-")
    print(" running pow Tests on: " + sys.platform)
    print(" ... ")
    if sys.platform.startswith("darwin"):
        # osx
        ret = pytest.main(["-k-notonosx", "pow_tests.py"])
    else:
        ret = pytest.main(["pow_tests.py"])
    
    print(" Failures: " +str(ret))
    print(55*"-")
    

