#
# Pow Default Tests
# 
#
# runtest script.
# runs test with respect to some paramters
# currently only os 

import sys
import pytest

# possible sys.platform results:
# http://stackoverflow.com/questions/446209/possible-values-from-sys-platform

MODELNAME = "pow_test_model"
class TestClass:
    @pytest.mark.notonosx
    @pytest.mark.run(order=1)
    @pytest.mark.minimal
    def test_server(self):
        """ test if server starts
            calls baseurl:port/test/12 
            must return 12.
            This test the server, routing and method dispatching
        """
        print(" .. Test if server works" )        
        from multiprocessing import Process
        import {{appname}}.server
        import requests
        import {{appname}}.config as cfg
        import time
        p = Process(target={{appname}}.server.main)
        p.start()
        testurl=cfg.server_settings["protocol"] + cfg.server_settings["host"] + ":" + str(cfg.server_settings["port"]) + "/test/12"  

        r = requests.get(testurl)
        p.terminate()
        assert int(r.text)==12
    
    @pytest.mark.run(order=2)
    @pytest.mark.minimal
    def test_sql_generate_model(self):
        """ test if sql model is generated"""
        print(" .. Test generate_model")
        import {{appname}}.generate_model as gm
        import uuid
        import os.path
        ret = gm.generate_model(MODELNAME, "sql", appname="{{appname}}")
        # generate model returns true in case of success
        assert ret is True
        assert os.path.exists(os.path.normpath("../models/sql/" + MODELNAME + ".py"))

    @pytest.mark.run(order=3)
    @pytest.mark.minimal
    def test_sql_model_type(self):
        """ based on test_generate_model. Tests if a model can insert values 
            DB sqlite by default.
        """ 
        print(" .. Test model is correct type")
        from {{appname}}.models.sql.pow_test_model import PowTestModel
        m = PowTestModel()
        assert isinstance(m, PowTestModel)
    
    @pytest.mark.run(order=4)
    def test_sql_dbsetup(self):
        """ test the setup of the alembic environment """
        print(" .. Test SQL: db_setup")
        import {{appname}}.init_sqldb_environment
        import os
        os.chdir("..")
        r = {{appname}}.init_sqldb_environment.init_migrations()
        assert r == True
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
    
    @pytest.mark.run(order=5)
    def test_sql_migration(self):
        """ test the setup of the alembic environment """
        print(" .. Test SQL: generate_migration")
        import {{appname}}.generate_migration
        import os
        os.chdir("..")
        script = {{appname}}.generate_migration.generate_migration(message="pow_test")
        assert os.path.exists(os.path.normpath(script.path))
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
    
    @pytest.mark.run(order=6)
    def test_sql_dbupdate(self):
        """ test the setup of the alembic environment """
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
    
    @pytest.mark.run(order=7)
    def test_sql_insert_and_find(self):
        """ based on test_generate_model. Tests if a model can insert values 
            and can be found back.
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

    #
    # tinyDB tests
    #
    @pytest.mark.run(order=8)
    @pytest.mark.minimal
    def test_tinydb_generate_model(self):
        """ test if sql model is generated"""
        print(" .. Test tinyDB generate_model")
        import {{appname}}.generate_model as gm
        import uuid
        import os.path
        ret = gm.generate_model(MODELNAME, "tinydb", appname="{{appname}}")
        # generate model returns true in case of success
        assert ret is True
        assert os.path.exists(os.path.normpath("../models/tinydb/" + MODELNAME + ".py"))

    @pytest.mark.run(order=9)
    @pytest.mark.minimal
    def test_tinydb_model_type(self):
        """ based on test_generate_model. Tests if a model can insert values 
            DB sqlite by default.
        """ 
        print(" .. Test model tinyDB is correct type")
        from {{appname}}.models.tinydb.pow_test_model import PowTestModel
        m = PowTestModel()
        assert isinstance(m, PowTestModel)
    
    @pytest.mark.run(order=10)
    def test_tinydb_insert_and_find(self):
        """ based on test_generate_model. Tests if a model can insert values 
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
    

