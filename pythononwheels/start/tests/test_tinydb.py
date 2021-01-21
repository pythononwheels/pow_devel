#
# Pow TinyDB Tests
# 
#
# runtest script.
# runs test with respect to some paramters


import sys
import pytest
import time

#
# tinyDB tests
#
@pytest.mark.run(order=1)
@pytest.mark.minimal
def test_tinydb_generate_model(modelname):
    """ test if sql model is generated"""
    print(" .. Test tinyDB generate_model")
    import {{appname}}.generate_model as gm
    import uuid
    import os.path
    ret = gm.generate_model(modelname, "tinydb", appname="{{appname}}")
    # generate model returns true in case of success
    assert ret is True
    assert os.path.exists(os.path.normpath("../models/tinydb/" + modelname + ".py"))

@pytest.mark.run(order=2)
@pytest.mark.minimal
def test_if_tinydb_model_validation_works():
    """ 
        check if validation works
    """ 
    print(" .. Test SQL: model validation() method")
    from {{appname}}.models.tinydb.pow_test_model import PowTestModel
    m = PowTestModel()
    assert m.validate() == True

@pytest.mark.run(order=3)
@pytest.mark.minimal
def test_if_tinydb_model_validation_fails_successfully():
    """ 
        check if validation fails if constraint is violated 
    """ 
    print(" .. Test SQL: modelcheck if validation fails if constraint is violated (maxlength)")
    from {{appname}}.models.tinydb.pow_test_model import PowTestModel
    m = PowTestModel()
    m.title="123456789123456789123456789123456789"
    assert m.validate() == False

@pytest.mark.run(order=4)
@pytest.mark.minimal
def test_tinydb_model_type():
    """ 
        Tests if generated Model has the right type
    """ 
    print(" .. Test model tinyDB is correct type")
    from {{appname}}.models.tinydb.pow_test_model import PowTestModel
    m = PowTestModel()
    assert isinstance(m, PowTestModel)

@pytest.mark.run(order=5)
def test_tinydb_insert_and_find():
    """ 
        based on test_generate_model. Tests if a model can insert values 
        and can be found back.
    """ 
    print(" .. Test tinyDB: model.upsert() and model.find()")
    from {{appname}}.models.tinydb.pow_test_model import PowTestModel
    import os
    m = PowTestModel()
    m.title = "TestnamePowTestRunner"
    m.upsert()
    res=m.find(m.Query.title=="TestnamePowTestRunner")
    assert res
    m.db.close()
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
    